from datetime import datetime

from movesense_bt.timestamp_to_utf import TimestampConverter


class NotificationHandler:
    def __init__(self):
        self.timestamp_converter = TimestampConverter()

    def reset_timestamps(self):
        self.timestamp_converter = TimestampConverter()

    async def notification_handler_imu(self, _, dv, data_storage, diff):
        """Notification handler for one of IMU sensors"""
        samples = 8
        val = []

        # Dig data from the binary
        timestamp = dv.get_uint_32(0)
        converted_timestamp = self.timestamp_converter.convert_timestamp(timestamp)

        for i in range(0, samples):
            imu_val = []
            for j in range(0, 9):
                if j in (0, 1, 2, 6, 7, 8):
                    imu_val.append(dv.get_int_16(4 + i * 18 + (j * 2)) / 100.0)
                else:
                    imu_val.append(dv.get_int_16(4 + i * 18 + (j * 2)) / 10.0)

            # Adding data to dataframe for later saving
            val.append(imu_val)
            data_storage.append([converted_timestamp + (diff * i)] + val[i])

    async def notification_handler_ecg(self, _, dv, data_storage, diff):
        """Simple notification handler for ECG sensor"""
        val = []
        samples = 16

        # Dig data from the binary
        timestamp = dv.get_uint_32(0)
        converted_timestamp = self.timestamp_converter.convert_timestamp(timestamp)

        info_string = "ecg" + str(converted_timestamp)

        for i in range(0, samples):
            val.append(dv.get_int_16(4 + 2 * i))
            # Adding data to dataframe for later saving
            data_storage.append([converted_timestamp + (diff * i), val[i]])
            info_string += ',ecg' + str(val[i])

    async def notification_handler_hr(self, _, dv, data_storage):
        """Simple notification handler for heartrate"""

        # Dig data from the binary
        hr = dv.get_uint_8(1)
        rr = dv.get_uint_16(2)

        timestamp = datetime.now().timestamp() * 1000

        data_storage.append([timestamp, hr, rr])