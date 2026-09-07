class SynchronizeGraphUseCase:

    def __init__(self, synchronization_service):
        self.synchronization_service = (
            synchronization_service
        )

    def execute(self):

        return (
            self.synchronization_service
            .synchronize()
        )
