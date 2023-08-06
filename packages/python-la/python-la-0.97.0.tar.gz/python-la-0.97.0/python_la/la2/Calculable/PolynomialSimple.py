from __future__ import annotations
from typing import Tuple, Union, Sequence
import functools
from .Calculable import Calculable
from ...la1 import Complex, Matrix, LinearMap
from ...utils import string_splitter, check_foreach, python_la_is_number, split_if_any, sign, almost_equal, newton_raphson, pretty_str
import math
from danielutils import validate, isoneof
from ...BaseClasses import PolynomialSimple____


class PolynomialSimple__(Calculable, PolynomialSimple____):
    @validate(None, Sequence, Sequence)
    def __init__(self, prefixes: Sequence, powers: Sequence) -> None:
        if len(prefixes) != len(powers):
            if len(prefixes) == 1 and len(powers) == 0 and prefixes[0] == 0:
                self.powers = []
                self.prefixes = []
                return
            raise ValueError("Prefixes and powers must be of same length")

        tuples = [(prefixes[i], powers[i]) for i in range(len(powers))]
        POW = 1
        PRE = 0

        def comparer(v1: Tuple, v2: Tuple) -> int:
            # TODO what if one of them is complex? __lt__ need to be implemented, but how?
            bias = 1
            if v1[POW] < v2[POW]:
                return -bias
            elif v1[POW] > v2[POW]:
                return bias
            else:
                if v1[PRE] < v2[PRE]:
                    return -bias
                elif v1[PRE] > v2[PRE]:
                    return bias
                else:
                    return 0

        tuples.sort(key=functools.cmp_to_key(comparer), reverse=True)
        powers = [tuples[i][POW]
                  for i in range(len(tuples)) if tuples[i][PRE] != 0]
        prefixes = [tuples[i][PRE]
                    for i in range(len(tuples)) if tuples[i][PRE] != 0]
        self.prefixes = []
        self.powers = []
        i = 0
        while i < len(powers):
            p = powers[i]
            count = powers.count(p)
            if count > 1:
                r = range(i, i+count)
                sum = 0
                for j in r:
                    sum += prefixes[j]
                    i += 1
                i -= 1
                self.prefixes.append(sum)
                self.powers.append(p)
            else:
                self.prefixes.append(prefixes[i])
                self.powers.append(p)
            i += 1

        check = True
        for p in self.prefixes:
            if p != 0:
                check = False
                break
        if check:
            self.prefixes = [0]
            self.powers = [0]
        else:
            self.powers = [self.powers[i]
                           for i in range(len(self.powers)) if self.prefixes[i] != 0]
            self.prefixes = [self.prefixes[i]
                             for i in range(len(self.prefixes)) if self.prefixes[i] != 0]

    def __str__(self) -> str:
        def one_to_str(i: int) -> str:
            power = self.powers[i]
            if power == int(power):
                power = int(power)
            prefix = self.prefixes[i]
            if prefix == int(prefix):
                prefix = int(prefix)
            res = ""

            if prefix == 0:
                return ""
            elif abs(prefix) == 1:
                if power == 0:
                    return "+1"
                if prefix == 1:
                    return "+X" if power == 1 else "+X^" + str(power)
                else:
                    return "-X" if power == 1 else "-X^" + str(power)
            else:
                if prefix >= 0:
                    res += "+"
                res += str(prefix)

            if power == 0:
                return res
            elif power == 1:
                return res+"X"
            return f"{res}X^{str(power)}"
        res = " ".join([one_to_str(i) for i in range(len(self))])
        if self.prefixes[0] > 0:
            res = res[1:]
        return pretty_str(res)

    @validate(None, [int, float, Complex, PolynomialSimple____])
    def __add__(self, other) -> PolynomialSimple:
        if isoneof(other, [int, float, Complex]):
            if other == 0:
                return PolynomialSimple(self.prefixes, self.powers)
            elif 0 in self.powers:
                index = self.powers.index(0)
                if self.prefixes[index] + other == 0:
                    return PolynomialSimple(self.prefixes[:index]+self.prefixes[index+1:], self.powers[:index]+self.powers[index+1:])
                new_prefixes = self.prefixes[:index] + \
                    [self.prefixes[index] + other] + self.prefixes[index+1:]
                return PolynomialSimple(new_prefixes, self.powers)
            return PolynomialSimple(self.prefixes+[other], self.powers+[0])
        elif isinstance(other, PolynomialSimple):
            return PolynomialSimple(self.prefixes+other.prefixes, self.powers+other.powers)
        raise NotImplementedError(
            f"Polynomial addition not implemented for {type(other)}")

    def __radd__(self, other) -> PolynomialSimple:
        return self.__add__(other)

    def __sub__(self, other) -> PolynomialSimple:
        return self.__add__(-other)

    def __rsub__(self, other) -> PolynomialSimple:
        return other + (-self)

    def __neg__(self) -> PolynomialSimple:
        return self*(-1)

    @validate(None, [int, float, Complex, PolynomialSimple____, Matrix])
    def __mul__(self, other) -> Union[PolynomialSimple, Matrix]:
        if isoneof(other, [int, float, Complex]):
            return PolynomialSimple([other*pre for pre in self.prefixes], self.powers)
        elif isinstance(other, PolynomialSimple):
            new_prefixes, new_powers = [], []
            for i in range(len(other)):
                for j in range(len(self)):
                    new_prefixes.append(self.prefixes[j]*other.prefixes[i])
                    new_powers.append(self.powers[j]+other.powers[i])
            return PolynomialSimple(new_prefixes, new_powers)
        elif isinstance(other, Matrix):
            return other*self

    def __rmul__(self, other) -> PolynomialSimple:
        return self.__mul__(other)

    @validate(None, [int, float, Complex, PolynomialSimple____])
    def __truediv__(self, other) -> Tuple[PolynomialSimple, PolynomialSimple]:
        if self == other:
            return PolynomialSimple([1], [0]), 0
        if isoneof(other, [int, float, Complex]):
            return self*(1/other), 0
        elif isinstance(other, PolynomialSimple):
            if self.degree >= other.degree and len(self) > len(other):
                quotient, remainder = PolynomialSimple([0], [0]), None
                current = self
                prefix, power = 1, 1
                while (current.degree >= other.degree):
                    prefix = current.prefixes[0]/other.prefixes[0]
                    power = current.powers[0] - other.powers[0]
                    current_quotient = PolynomialSimple([prefix], [power])
                    quotient += current_quotient
                    subtructor = current_quotient*other
                    # PolynomialSimple(
                    # [quotient.prefixes[-1]*v for v in other.prefixes], [quotient.prefixes[-1]*v for v in other.powers])
                    current -= subtructor
                remainder, _ = current/other
                return quotient, remainder
            else:
                if self.degree == 0:
                    return self.prefixes[0]/other, 0
                return None, 0
        # TODO need to add?
        raise NotImplementedError("Polynomial division not implemented")

    def __rtruediv__(self, other) -> PolynomialSimple:
        if isoneof(other, [int, float, Complex]):
            pass
        elif isinstance(other, PolynomialSimple):
            pass

    @validate(None, int)
    def __pow__(self, pow) -> PolynomialSimple:
        if isinstance(pow, int):
            if pow == 0:
                return PolynomialSimple([1], [0])
            res = self
            for _ in range(abs(pow)-1):
                res *= self
            if pow < 0:
                return 1/res
            return res

    @validate(None, [int, float, Complex, PolynomialSimple____])
    def __eq__(self, other: PolynomialSimple) -> bool:
        if isoneof(other, [int, float, Complex]):
            if other == 0:
                return all([v == 0 for v in self.prefixes])
            if len(self) != 1:
                return False
            return self.powers[0] == 0 and self.prefixes[0] == other
        if isinstance(other, PolynomialSimple):
            if len(self) != len(other):
                return False
            for i in range(len(self)):
                if self.prefixes[i] != other.prefixes[i] or self.powers[i] != other.powers[i]:
                    return False
            return True
        raise NotImplementedError(
            f"Polynomial equality not implemented for {type(other)}")

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __call__(self, v):
        from .PolynomialFraction import PolynomialFraction
        if not isoneof(v, [int, float, Complex, PolynomialSimple, Matrix, LinearMap, PolynomialFraction]):
            # TODO implement __call_ for matrix,operator,vector,etc
            raise NotImplementedError(
                "Polynomial __call__ not implemented for " + str(type(v)))
        res = self.prefixes[0]*v**self.powers[0]
        diff = 0
        if isinstance(v, Matrix) and 0 in self.powers:
            diff = 1
        for i in range(1, len(self)-diff):
            res += self.prefixes[i]*v**self.powers[i]
        if isinstance(v, Matrix) and 0 in self.powers:
            res += self.prefixes[-1] * Matrix.identity(len(v))
        return res

    def __len__(self) -> int:
        return len(self.powers)


class PolynomialSimple(PolynomialSimple__):
    @staticmethod
    @validate(str, str)
    def from_string(input: str, var: str = "x") -> PolynomialSimple:
        # FIXME "x-1" == "x+1" which is not good
        if var not in input:
            for c in input:
                if not c.isdigit():
                    raise ValueError("")
            return PolynomialSimple([float(input)], [0])
        # --------helper functions----------

        def sub_to_poly(sub) -> PolynomialSimple:
            def pow_to_poly(subb: str) -> PolynomialSimple:
                individual_chars = string_splitter([subb], "^")
                if len(individual_chars) == 2:
                    if var not in subb:
                        a, b = individual_chars[0], individual_chars[1]
                        if check_foreach([a, b], python_la_is_number):
                            return PolynomialSimple([(float(a))**(float(b))], [0])

                    bias = 1

                    def extract_nums(indiv) -> Tuple[float, float]:
                        try:
                            power = float(indiv[bias % 2])
                            prefix = 1
                            if indiv[(bias+1) % 2] != var:
                                prefix = float(
                                    indiv[(bias+1) % 2].replace(var, ""))
                            return prefix, power
                        except Exception as e:
                            raise e

                    prefix, power = 1, 0
                    try:
                        prefix, power = extract_nums(individual_chars)
                    except ValueError as e:
                        bias += 1
                        prefix, power = extract_nums(individual_chars)
                    return PolynomialSimple([prefix], [power])

                elif len(individual_chars) == 1:
                    text = individual_chars[0]
                    if text == var:
                        return PolynomialSimple([1], [1])
                    prefix = float(text.replace(var, ""))
                    return PolynomialSimple([prefix], [1 if var in text else 0])
                assert False, "didnt think about that"

            subs2, multiplication_stack = split_if_any(sub, ["*", "/"])
            res = pow_to_poly(subs2[0])
            for i, s in enumerate(subs2[1:]):
                if multiplication_stack[i] == "*":
                    res *= pow_to_poly(s)
                elif multiplication_stack[i] == "/":
                    res /= pow_to_poly(s)

            return res

        # handle if input has brackets
        if any(bracket in input for bracket in ["(", ")", "[", "]", "{", "}"]):
            raise ValueError("PolynomialSimple doesnt support brackets")
            # if not validate_brackets(input):
            #     raise ValueError("invalid brackets")
            # input = open_power(input)
            # sub_inputs = split_not_between_brackets(input, "*")
            # res = PolynomialSimple.from_string(sub_inputs[0], var)
            # for sub_input in sub_inputs[1:]:
            #     res *= PolynomialSimple.from_string(sub_input, var)
            # return res
        # split with addition
        subs, order = split_if_any(input, ["+", "-"])
        if len(order) < len(subs):
            order.insert(0, "+")
        # foreach sub expression create a Poly with inner splitting by multiplication and add it acording to current addition operator
        res = sign(order[0])*sub_to_poly(subs[0])
        for i in range(1, len(subs)):
            res += sign(order[i])*sub_to_poly(subs[i])
        return res

    @property
    def roots(self) -> list:
        res = []
        curr = self
        if 0 not in self.powers:
            lowest_power = self.powers[-1]
            res += [0 for _ in range(lowest_power)]
            curr = PolynomialSimple(
                self.prefixes, [v-lowest_power for v in self.powers])
        if curr.degree == 0:
            return res
        if curr.degree == 1:
            if 0 in curr.powers:
                return res+[-curr.prefixes[-1]]
            return res+[0]
        elif curr.degree == 2:
            a, b, c = 0, 0, 0
            a = curr.prefixes[curr.powers.index(2)]
            if 1 in curr.powers:
                b = curr.prefixes[curr.powers.index(1)]
            if 0 in curr.powers:
                c = curr.prefixes[curr.powers.index(0)]
            delta = b**2 - 4*a*c
            x1, x2 = 0, 0
            if delta < 0:
                img = Complex(0, math.sqrt(abs(delta)))
                x1 = -b+img
                x2 = -b-img
            else:
                x1 = -b+math.sqrt(delta)
                x2 = -b-math.sqrt(delta)
            x1 /= 2*a
            x2 /= 2*a
            return res+[x1, x2]

        x = 1
        der = curr.derivative
        count = 0
        MAX_COUNT = 100
        while not almost_equal(0, curr(x)) and count < MAX_COUNT:
            x = newton_raphson(curr, x, der)
            count += 1
        if count == MAX_COUNT:
            return []
        res += [x]
        remainder, _ = curr / PolynomialSimple.from_string(f"x-{x}")
        res += remainder.roots
        return res

    @property
    def degree(self) -> float:
        return self.powers[0] if len(self.powers) > 0 else 0

    @property
    def derivative(self) -> PolynomialSimple:
        if self.degree == 0:
            return PolynomialSimple([0], [0])
        return PolynomialSimple([self.prefixes[i]*self.powers[i] for i in range(len(self.powers))], [self.powers[i] - 1 for i in range(len(self.powers))])

    @property
    def integral(self) -> PolynomialSimple:
        if self.degree == 0:
            return PolynomialSimple([0], [0])
        return PolynomialSimple([self.prefixes[i]/(self.powers[i]+1) for i in range(len(self.powers))], [self.powers[i] + 1 for i in range(len(self.powers))])

    @validate(None, PolynomialSimple__)
    def solve(self, solve_for: PolynomialSimple = 0) -> list:
        if not isinstance(solve_for, PolynomialSimple):
            raise TypeError("solve_for must be a PolynomialSimple")
        return (self-solve_for).roots

    @validate(None, PolynomialSimple__)
    def gcd_with(self, other: PolynomialSimple) -> PolynomialSimple:
        def intersection(lst1, lst2):
            return [value for value in set(lst1) if value in set(lst2)]
        common_roots = intersection(self.roots, other.roots)
        res = 1
        for root in common_roots:
            if root < 0:
                res *= PolynomialSimple.from_string(f"x+{abs(root)}")
            else:
                res *= PolynomialSimple.from_string(f"x-{root}")
        return res
