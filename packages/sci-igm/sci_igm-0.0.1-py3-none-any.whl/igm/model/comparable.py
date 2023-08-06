from operator import lt, le, gt, ge, eq


class Comparable:
    """
    Overview:
        Base class of linear comparable objects.
    """

    def _value(self):
        """
        Linear value of this object.
        """
        raise NotImplementedError  # pragma: no cover

    def _cmp_preprocess(self, other):
        """
        Preprocess function of another object.

        :param other: Original object.
        :return: Preprocessed object.
        :raise ValueError,TypeError: Raised when not able to preprocess, \
            the comparison will return ``False`` directly.
        """
        return type(self)(other)

    def _cmp_precondition(self, other):
        """
        Precondition of comparison.

        :param other: Another object.
        :return: Precondition is satisfied or not.
        """
        return type(self) == type(other)

    def _cmp(self, cmp, other):
        try:
            other = self._cmp_preprocess(other)
        except (ValueError, TypeError):
            return False

        if self._cmp_precondition(other):
            return cmp(self._value(), other._value())
        else:
            return False

    def __lt__(self, other):
        return self._cmp(lt, other)

    def __le__(self, other):
        return self._cmp(le, other)

    def __gt__(self, other):
        return self._cmp(gt, other)

    def __ge__(self, other):
        return self._cmp(ge, other)

    def __eq__(self, other):
        return self._cmp(eq, other)
