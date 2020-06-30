from proglog import ProgressBarLogger


class VideoProgressLogger(ProgressBarLogger):

    def __init__(self, task):
        self.task = task
        super(VideoProgressLogger, self).__init__()

    def callback(self, **changes):
        bars = self.state.get('bars')
        index = len(bars.values()) - 1
            
        if index > -1:
            bar = list(bars.values())[index]
            progress = int(bar["index"] / bar["total"] * 100)

            if bar["title"] == 't':
                self.task.update_state(state="PROGRESS", meta={
                    'current': progress, "total": 100, "status": "Processing video"})
            else:
                self.task.update_state(state="PROGRESS", meta={
                    'current': progress, "total": 100, "status": "Processing audio"})
