# The MIT License (MIT)
# Copyright © 2024 Nimble Labs Ltd

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from typing import Union

# import nimble


class Balance:
    """
    Represents the nimble balance of the wallet, stored as vim (int).
    This class provides a way to interact with balances in two different units: vim and nim.
    It provides methods to convert between these units, as well as to perform arithmetic and comparison operations.

    Attributes:
        unit: A string representing the symbol for the nim unit.
        vim_unit: A string representing the symbol for the vim unit.
        vim: An integer that stores the balance in vim units.
        nim: A float property that gives the balance in nim units.
    """

    unit: str = 'nim'  # This is the nim unit
    vim_unit: str = chr(0x03C1)  # This is the vim unit
    vim: int
    nim: float

    def __init__(self, balance: Union[int, float]):
        """
        Initialize a Balance object. If balance is an int, it's assumed to be in vim.
        If balance is a float, it's assumed to be in nim.

        Args:
            balance: The initial balance, in either vim (if an int) or nim (if a float).
        """
        if isinstance(balance, int):
            self.vim = balance
        elif isinstance(balance, float):
            # Assume nim value for the float
            self.vim = int(balance * pow(10, 9))
        else:
            raise TypeError("balance must be an int (vim) or a float (nim)")

    @property
    def nim(self):
        return self.vim / pow(10, 9)

    def __int__(self):
        """
        Convert the Balance object to an int. The resulting value is in vim.
        """
        return self.vim

    def __float__(self):
        """
        Convert the Balance object to a float. The resulting value is in nim.
        """
        return self.nim

    def __str__(self):
        """
        Returns the Balance object as a string in the format "symbolvalue", where the value is in nim.
        """
        return f"{self.unit}{float(self.nim):,.9f}"

    def __rich__(self):
        return "[green]{}[/green][green]{}[/green][green].[/green][dim green]{}[/dim green]".format(
            self.unit,
            format(float(self.nim), "f").split(".")[0],
            format(float(self.nim), "f").split(".")[1],
        )

    def __str_vim__(self):
        return f"{self.vim_unit}{int(self.vim)}"

    def __rich_vim__(self):
        return f"[green]{self.vim_unit}{int(self.vim)}[/green]"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other: Union[int, float, "Balance"]):
        if other is None:
            return False

        if hasattr(other, "vim"):
            return self.vim == other.vim
        else:
            try:
                # Attempt to cast to int from vim
                other_vim = int(other)
                return self.vim == other_vim
            except (TypeError, ValueError):
                raise NotImplementedError("Unsupported type")

    def __ne__(self, other: Union[int, float, "Balance"]):
        return not self == other

    def __gt__(self, other: Union[int, float, "Balance"]):
        if hasattr(other, "vim"):
            return self.vim > other.vim
        else:
            try:
                # Attempt to cast to int from vim
                other_vim = int(other)
                return self.vim > other_vim
            except ValueError:
                raise NotImplementedError("Unsupported type")

    def __lt__(self, other: Union[int, float, "Balance"]):
        if hasattr(other, "vim"):
            return self.vim < other.vim
        else:
            try:
                # Attempt to cast to int from vim
                other_vim = int(other)
                return self.vim < other_vim
            except ValueError:
                raise NotImplementedError("Unsupported type")

    def __le__(self, other: Union[int, float, "Balance"]):
        try:
            return self < other or self == other
        except TypeError:
            raise NotImplementedError("Unsupported type")

    def __ge__(self, other: Union[int, float, "Balance"]):
        try:
            return self > other or self == other
        except TypeError:
            raise NotImplementedError("Unsupported type")

    def __add__(self, other: Union[int, float, "Balance"]):
        if hasattr(other, "vim"):
            return Balance.from_vim(int(self.vim + other.vim))
        else:
            try:
                # Attempt to cast to int from vim
                return Balance.from_vim(int(self.vim + other))
            except (ValueError, TypeError):
                raise NotImplementedError("Unsupported type")

    def __radd__(self, other: Union[int, float, "Balance"]):
        try:
            return self + other
        except TypeError:
            raise NotImplementedError("Unsupported type")

    def __sub__(self, other: Union[int, float, "Balance"]):
        try:
            return self + -other
        except TypeError:
            raise NotImplementedError("Unsupported type")

    def __rsub__(self, other: Union[int, float, "Balance"]):
        try:
            return -self + other
        except TypeError:
            raise NotImplementedError("Unsupported type")

    def __mul__(self, other: Union[int, float, "Balance"]):
        if hasattr(other, "vim"):
            return Balance.from_vim(int(self.vim * other.vim))
        else:
            try:
                # Attempt to cast to int from vim
                return Balance.from_vim(int(self.vim * other))
            except (ValueError, TypeError):
                raise NotImplementedError("Unsupported type")

    def __rmul__(self, other: Union[int, float, "Balance"]):
        return self * other

    def __truediv__(self, other: Union[int, float, "Balance"]):
        if hasattr(other, "vim"):
            return Balance.from_vim(int(self.vim / other.vim))
        else:
            try:
                # Attempt to cast to int from vim
                return Balance.from_vim(int(self.vim / other))
            except (ValueError, TypeError):
                raise NotImplementedError("Unsupported type")

    def __rtruediv__(self, other: Union[int, float, "Balance"]):
        if hasattr(other, "vim"):
            return Balance.from_vim(int(other.vim / self.vim))
        else:
            try:
                # Attempt to cast to int from vim
                return Balance.from_vim(int(other / self.vim))
            except (ValueError, TypeError):
                raise NotImplementedError("Unsupported type")

    def __floordiv__(self, other: Union[int, float, "Balance"]):
        if hasattr(other, "vim"):
            return Balance.from_vim(int(self.nim // other.nim))
        else:
            try:
                # Attempt to cast to int from vim
                return Balance.from_vim(int(self.vim // other))
            except (ValueError, TypeError):
                raise NotImplementedError("Unsupported type")

    def __rfloordiv__(self, other: Union[int, float, "Balance"]):
        if hasattr(other, "vim"):
            return Balance.from_vim(int(other.vim // self.vim))
        else:
            try:
                # Attempt to cast to int from vim
                return Balance.from_vim(int(other // self.vim))
            except (ValueError, TypeError):
                raise NotImplementedError("Unsupported type")

    def __int__(self) -> int:
        return self.vim

    def __float__(self) -> float:
        return self.nim

    def __nonzero__(self) -> bool:
        return bool(self.vim)

    def __neg__(self):
        return Balance.from_vim(-self.vim)

    def __pos__(self):
        return Balance.from_vim(self.vim)

    def __abs__(self):
        return Balance.from_vim(abs(self.vim))

    @staticmethod
    def from_float(amount: float):
        """
        Given nim (float), return Balance object with vim(int) and nim(float), where vim = int(nim*pow(10,9))
        Args:
            amount: The amount in nim.

        Returns:
            A Balance object representing the given amount.
        """
        vim = int(amount * pow(10, 9))
        return Balance(vim)

    @staticmethod
    def from_nim(amount: float):
        """
        Given nim (float), return Balance object with vim(int) and nim(float), where vim = int(nim*pow(10,9))

        Args:
            amount: The amount in nim.

        Returns:
            A Balance object representing the given amount.
        """
        vim = int(amount * pow(10, 9))
        return Balance(vim)

    @staticmethod
    def from_vim(amount: int):
        """
        Given vim (int), return Balance object with vim(int) and nim(float), where vim = int(nim*pow(10,9))

        Args:
            amount: The amount in vim.

        Returns:
            A Balance object representing the given amount.
        """
        return Balance(amount)
