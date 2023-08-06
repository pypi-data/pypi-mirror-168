from friendly_traceback.info_generic import register
from pandas.errors import SettingWithCopyWarning


@register(SettingWithCopyWarning)
def setting_with_copy_warning() -> str:
    return ("Pandas occasionally emits a `SettingWithCopyWarning` when you use 'chained indexing',\n"
            "either directly or indirectly,"
             "and you then attempt to assign a value to the result.\n"
             "By 'direct chained indexing', we mean that your code contains something like:\n\n"
             "    ...[index_1][index_2] = ...\n"
             "During the first extraction using `[index_1]`, pandas found that the series to be created\n"
             "contained values of different types. It automatically created a new series\n"
             "converting all values to a common type.\n"
             "The second indexing, `[index_2]` was then done a this copy\n"
             "instead of the original dataframe.\n"
             "Thus, the assigment was not done on the original dataframe, which caused Pandas to emit this warning.\n\n"
             "An 'indirect chained indexing' essentially amount to the same problem except that\n"
             "the second indexing is not done on the same line as that which was done\n"
             "to extract the first series.\n"
             )
