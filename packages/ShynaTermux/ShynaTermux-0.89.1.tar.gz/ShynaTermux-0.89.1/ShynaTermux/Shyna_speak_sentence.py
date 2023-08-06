from ShynaDatabase import Shdatabase
from ShynaProcess import ShynaSpeak


class ShynaSpeakOnTermux:
    """
    Get sentences from database and speak them as needed
    """
    s_data = Shdatabase.ShynaDatabase()
    s_process = ShynaSpeak.ShynaSpeak()

    def get_sentences(self):
        try:
            self.s_data.query = "Select sent_speak,count from termux_speak where status='False' order by count DESC limit 1"
            result = self.s_data.select_from_table()
            if str(result[0]).lower().__eq__('empty'):
                pass
            else:
                self.s_process.shyna_speaks_termux(msg=str(result[0][0]))
        except Exception as e:
            print(e)
        finally:
            self.s_data.query = "Update termux_speak set status='True' where count='"+str(result[0][1])+"'"
            self.s_data.create_insert_update_or_delete()


if __name__ == '__main__':
    ShynaSpeakOnTermux().get_sentences()
