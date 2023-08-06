import os
from re import match, split, sub


class Helper(object):
    @staticmethod
    def get_base_path():
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
        return path

    @staticmethod
    def camel_case(string: str) -> str:
        """
        This method intends to get a string and convert it to camel case.

        :param string: the string that will be converted
        :type string: str

        :return: a camel case string
        :rtype: str
        """
        if match(pattern=r"[A-Z][a-z]+[A-Z][a-z]+", string=string) is not None:
            return string
        else:
            string = sub(pattern="[çÇ]", repl="c", string=string)
            string = sub(pattern="[áàãâÁÀÃÂ]", repl="a", string=string)
            string = sub(pattern="[éèêÉÈÊ]", repl="e", string=string)
            string = sub(pattern="[ìíîÍÌÎ]", repl="i", string=string)
            string = sub(pattern="[õôóòÕÔÓÒ]", repl="o", string=string)
            string = sub(pattern="[úùûÚÙÛ]", repl="u", string=string)
            string = (
                sub(pattern=r"[,._-]", repl=" ", string=string).title().replace(" ", "")
            )
            return string

    @staticmethod
    def capitalize_first_letter(string: str) -> str:
        """
        This method intends to capitalize every first letter of the list of words as string and return the joined string.

        :param string: the string that will be converted
        :type string: str

        :return: the string with all first letters of the words capitalized
        :rtype: str
        """
        if string:
            string = list(string)
            string[0] = string[0].capitalize()
            string = "".join(string)
        return string

    @staticmethod
    def snake_case(string: str) -> str:
        """
        This method intends to get a string and convert it to snake case.

        :param string: the string that will be converted
        :type string: str

        :return: a snake case string
        :rtype: str
        """
        string = "_".join(
            Helper.capitalize_first_letter(w) for w in split(" |_|-", string)
        )

        string = sub("ç", "c", string)
        string = sub("Ç", "C", string)

        string = sub("[áàãâ]", "a", string)
        string = sub("[ÁÀÃÂ]", "A", string)

        string = sub("[éèê]", "e", string)
        string = sub("[ÉÈÊ]", "E", string)

        string = sub("[ìíî]", "i", string)
        string = sub("[ÌÍÎ]", "I", string)

        string = sub("[õôóò]", "o", string)
        string = sub("[ÓÒÔÕ]", "O", string)

        string = sub("[úùû]", "u", string)
        string = sub("[ÚÙÛ]", "U", string)

        string = sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
        string = sub("__([A-Z])", r"_\1", string)
        string = sub("([a-z0-9])([A-Z])", r"\1_\2", string).lower()
        string = sub("[^a-z0-9_]", "", string).lstrip("_").rstrip("_")
        return string
