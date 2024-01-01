class _const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("can't change const %s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
        self.__dict__[name] = value


const = _const()
const.EXCEL_FILE_PREFIX = "CSVFilter_"
const.EXCEL_FILE_SUFFIX = ".xlsx"
const.EXCEL_FILE_PREFIX_UPGRADE_BOX = "CSVFilter_UpgradeBox_"
const.EXCEL_FILE_PREFIX_IOT_CORE = "CSVFilter_IotCore_"
const.MERGE_FILE_SHEET_NAME_ROW_DATA = "原始数据row_data"
const.MERGE_FILE_SHEET_NAME_IOT_DATA = "iot板数据iot_board_data"
const.MERGE_FILE_SHEET_NAME_BOX_DATA = "升级盒子数据box_data"
