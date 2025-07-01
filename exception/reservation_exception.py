class ReservationException(Exception):
    def __init__(self, message="Reservation error occurred"):
        self.message = message
        super().__init__(self.message)