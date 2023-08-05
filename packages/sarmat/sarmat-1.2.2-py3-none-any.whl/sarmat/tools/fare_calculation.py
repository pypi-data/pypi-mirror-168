"""
Sarmat.

Вспомогательные инструменты.

Расчет стоимости проезда
"""
import collections
import json
import re
import subprocess
import sys
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple

from sarmat.core.behavior import BhRoute
from sarmat.core.exceptions import WrongValueError, ImpossibleOperationError

from .fare_containers import FareArguments, FareContainer
from .json_encoder import SarmatEncoder, as_enum


class CalculationStrategy(ABC):
    """Абстрактный класс расчета стоимости"""
    accuracy = Decimal(10) ** -2

    @abstractmethod
    def make_base_calculation(self, args: FareArguments) -> Decimal:
        """
        Вычисление базовой стоимости проезда
        Args:
            args: аргументы для выполнения расчета

        Returns: стоимость проезда

        """


class FixPriceStrategy(CalculationStrategy):
    """Стратегия расчета стоимости по фиксированным значениям"""

    def __init__(self, price_map: List[Optional[List[Decimal]]]):
        self._price_map = price_map

    def make_base_calculation(self, args: FareArguments) -> Decimal:
        try:
            price = self._price_map[args.point_from][args.point_to]
        except IndexError:
            raise WrongValueError("Заданные индексы выходят за пределы массива")

        if price is None:
            raise ImpossibleOperationError("Для указанной пары пунктов нет рассчетного значения")

        return price.quantize(self.accuracy)


class AreaStrategy(CalculationStrategy):
    """Стратегия расчета стоимости по зонам"""

    def __init__(self, dimension: List[Any], price: List[Decimal]):
        if len(dimension) != len(price):
            raise WrongValueError("Размерность входных параметров должна совпадать")

        self._dimension = dimension
        self._price = price

    def make_base_calculation(self, args: FareArguments) -> Decimal:
        # NOTE: В python правая граница среза не входит в результат.
        #       Мы, указывая пункт назначения, включаем его в результат.
        #       Поэтому, при взятии среза необходимо добавлять к правой границе среза +1.
        destination_point = args.route[args.point_from:args.point_to+1]
        length = destination_point.len_from_start

        for idx, area in enumerate(self._dimension):
            if length < area:
                if idx == 0:
                    index = 0
                    break

            index = idx - 1
            break
        else:
            index = -1

        return self._price[index].quantize(self.accuracy)


class PKStrategy(CalculationStrategy):
    """Стратегия расчета стоимости по пассажиро/километрам"""

    def __init__(self, rate: Decimal):
        self._rate = Decimal(rate)

    def make_base_calculation(self, args: FareArguments) -> Decimal:
        # NOTE: В python правая граница среза не входит в результат.
        #       Мы, указывая пункт назначения, включаем его в результат.
        #       Поэтому, при взятии среза необходимо добавлять к правой границе среза +1.
        destination_point = args.route[args.point_from:args.point_to+1]
        length = destination_point.len_from_start

        return (length * self._rate).quantize(self.accuracy)


class PercentBaggageStrategy(CalculationStrategy):
    """Стратегия расчета стоимости провоза багажа как процент от посчитанной ранее стоимости"""

    def __init__(self, percent: Decimal):
        self._percent = Decimal(percent)

    def make_base_calculation(self, args: FareArguments) -> Decimal:
        price = args.base_pas_price
        return Decimal(price * self._percent / Decimal(100)).quantize(self.accuracy)


Code = collections.namedtuple("Code", "name code")


class FareCalculator:
    """Класс выполняет расчет стоимости проезда"""

    UTF8 = "utf-8"

    def __init__(self,
                 passenger_calc_strategy: CalculationStrategy,
                 baggage_calc_strategy: CalculationStrategy,
                 permanent_passenger_calc_script: Optional[str] = None,
                 volatile_passenger_calc_script: Optional[str] = None,
                 permanent_baggage_calc_script: Optional[str] = None,
                 volatile_baggage_calc_script: Optional[str] = None):
        """
        Args:
            passenger_calc_strategy: стратегия базового расчета стоимости проезда
            baggage_calc_strategy: стратегия базового расчета стоимости провоза багажа
            permanent_passenger_calc_script: расчет постоянных надбавок/скидок для стоимости проезда
            volatile_passenger_calc_script: расчет временных надбавок/скидок для стоимости проезда
            permanent_baggage_calc_script: расчет постоянных надбавок/скидок для стоимости провоза багажа
            volatile_baggage_calc_script: расчет временных надбавок/скидок для стоимости провоза багажа
        """
        self._passenger_strategy = passenger_calc_strategy
        self._baggage_strategy = baggage_calc_strategy
        self._permanent_pas_calc = None
        self._permanent_bag_calc = None
        self._volatile_pas_calc = None
        self._volatile_bag_script = None

        if permanent_passenger_calc_script:
            self._permanent_pas_calc = Code("Permanent passenger price calculation",
                                            permanent_passenger_calc_script)

        if permanent_baggage_calc_script:
            self._permanent_bag_calc = Code("Permanent baggage price calculation",
                                            permanent_baggage_calc_script)

        if volatile_passenger_calc_script:
            self._volatile_pas_calc = Code("Volatile passenger price calculation",
                                           volatile_passenger_calc_script)

        if volatile_baggage_calc_script:
            self._volatile_bag_calc = Code("Volatile baggage price calculation",
                                           volatile_baggage_calc_script)

    def _execute(self, code: Code, context: Dict[str, Any]) -> str:
        """Выполнение вычислений в отдельном подпроцессе
        Args:
            code: текст программного кода
            context: входные аргументы

        """
        module, offset = self._create_module(code.code, context)
        with subprocess.Popen([sys.executable, "-"],
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) as process:
            return self._communicate(process, code, module, offset)

    def _create_module(self, code: str, context: Dict[str, Any]) -> Tuple[str, int]:
        """Генерация модуля расчета смтоимости
        Args
            code: код модуля
            context: входные аргументы

        Returns:
            код, дополненный контекстными аргументами
            смещение строк

        """
        raw_context = json.dumps(context, cls=SarmatEncoder, )
        context_lines = [
            "import json",
            "from decimal import Decimal",
            "import sarmat",
            "from sarmat.tools.fare_containers import FareArguments",
            "from sarmat.tools.json_encoder import SarmatEncoder, as_enum",
            "",
            "null = None",
            f"context = FareArguments(**json.loads('''{raw_context}''', object_hook=as_enum))",
            code,
            "print(json.dumps(context.as_dict(), cls=SarmatEncoder))"
        ]
        offset = len(context_lines)
        return "\n".join(context_lines), offset

    def _communicate(self, process: subprocess.Popen, code: Code, module: str, offset: int) -> str:
        """Подключение к процессу, обработка результата
        Args:
            process: процесс
            code: контейнер с исходным кодом
            module: сформированный модуль
            offset: смещение строк после объявления переменных

        Returns: Вычисленная стоимость

        """
        stdout, stderr = process.communicate(module.encode(self.UTF8))

        if stderr:
            stderr = stderr.decode(self.UTF8).lstrip().replace(", in <module>", ":")
            stderr = re.sub(r", line (\d+)", lambda match: str(int(match.group(1)) - offset), stderr)
            message = re.sub(r'File."[^"]+?"', "'{}' has an error on line ".format(code.name), stderr)
            raise ImpossibleOperationError(message)

        if stdout:
            return stdout.decode(self.UTF8)

    def _calculate_base_passenger_price(self, args: FareArguments) -> None:
        """Расчет стоимости пассажирского билета
        Args:
            args: аргументы для выполнения расчета

        """
        args.base_pas_price = self._passenger_strategy.make_base_calculation(args)

    def _calculate_base_baggage_price(self, args: FareArguments) -> None:
        """Расчет стоимости багажного билета
        Args:
            args: аргументы для выполнения расчета

        """
        args.base_bag_price = self._baggage_strategy.make_base_calculation(args)

    def _calculate_permanent_add_passenger_price(self, args: FareArguments) -> FareArguments:
        """Расчет постоянной надбавки/скидки для пассажирского билета
        Args:
            args: аргументы для выполнения расчета

        """
        if self._permanent_pas_calc:
            raw_result = self._execute(self._permanent_pas_calc, args.as_dict())
            result = json.loads(f'{raw_result}', object_hook=as_enum)
            args = FareArguments(**result)

        return args

    def _calculate_volatile_add_passenger_price(self, args: FareArguments) -> FareArguments:
        """Расчет временной надбавки/скидки для пассажирского билета
        Args:
            args: аргументы для выполнения расчета

        """
        if self._volatile_pas_calc:
            raw_result = self._execute(self._volatile_pas_calc, args.as_dict())
            result = json.loads(raw_result, object_hook=as_enum)
            args = FareArguments(**result)

        return args

    def _calculate_permanent_add_baggage_price(self, args: FareArguments) -> FareArguments:
        """Расчет постоянной надбавки/скидки для багажного билета
        Args:
            args: аргументы для выполнения расчета

        """
        if self._permanent_bag_calc:
            raw_result = self._execute(self._permanent_bag_calc, args.as_dict())
            result = json.loads(raw_result, object_hook=as_enum)
            args = FareArguments(**result)

        return args

    def _calculate_volatile_add_baggage_price(self, args: FareArguments) -> FareArguments:
        """Расчет временной надбавки/скидки для багажного билета
        Args:
            args: аргументы для выполнения расчета

        """
        if self._volatile_bag_script:
            raw_result = self._execute(self._volatile_bag_calc, args.as_dict())
            result = json.loads(raw_result, object_hook=as_enum)
            args = FareArguments(**result)

        return args

    def _calculate_custom_passenger_price(self, args: FareArguments) -> None:
        """Вычисление прочих сумм для пассажирского билета"""
        args.customer_pas_price = {}

    def _calculate_custom_baggage_price(self, args: FareArguments) -> None:
        """Вычисление прочих сумм для багажного билета"""
        args.customer_bag_price = {}

    def calculate_price(self, route: BhRoute, point_from: int, point_to: int, **kwargs) -> FareContainer:
        """Вычисление стоимости проезда и провоза багажа"""
        args = FareArguments(route=route, point_from=point_from, point_to=point_to, other_arguments=kwargs)

        self._calculate_base_passenger_price(args)
        self._calculate_base_baggage_price(args)
        args = self._calculate_permanent_add_passenger_price(args)
        args = self._calculate_permanent_add_baggage_price(args)
        args = self._calculate_volatile_add_passenger_price(args)
        args = self._calculate_volatile_add_baggage_price(args)
        self._calculate_custom_passenger_price(args)
        self._calculate_custom_baggage_price(args)

        return FareContainer(
            base_passenger_price=args.base_pas_price,
            permanent_passenger_price=args.prm_pas_price,
            volatile_passenger_price=args.vlt_pas_price,
            base_baggage_price=args.base_bag_price,
            permanent_baggage_price=args.prm_bag_price,
            volatile_baggage_price=args.vlt_bag_price,
            custom_passenger_price=args.customer_pas_price,
            custom_baggage_price=args.customer_bag_price,
        )
