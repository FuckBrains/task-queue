from proglog import ProgressBarLogger


class VideoProgressLogger(ProgressBarLogger):

    def __init__(self, task):
        self.task = task
        super(VideoProgressLogger, self).__init__()

    def callback(self, **changes):
        # Every time the logger is updated, this function is called with
        # the `changes` dictionnary of the form `parameter: new value`.
        bars = self.state.get('bars')
        index = len(bars.values()) - 1
        if index > -1:
            bar = list(bars.values())[index]
            progress = int(bar['index'] / bar['total'] * 100)
            if bar["indent"] == 2:
                self.task.update_state(state="PROGRESS", meta={
                    'current': progress, "total": 100, "status": "Processing video"})
            else:
                self.task.update_state(state="PROGRESS", meta={
                    'current': 0, "total": 100, "status": "Preparing for processing"})
