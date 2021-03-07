class Config:
    activity = "Koi_Bot is operating normally!"
    prefix = ["//"]
    version = "Alpha 0.1"
    admin_id = [753625063357546556]

    def prefixes_no_space(self):
        ''' 접두사들을 띄어쓰기 없이 반환합니다. '''
        return [i.replace(' ', '') for i in self.prefix]