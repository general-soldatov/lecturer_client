from app.config.tickets import TicketOutput, TicketTemp
from app.connect.documents import WordDocument

class WordTicket(WordDocument):
    def __init__(self, tickets: TicketOutput, path_folder = None, path = "app/config/ticket.docx"):
        super().__init__(path_folder, path)
        self.type_doc = "Билеты"
        self.data = tickets.model_dump()

class WordQuestion(WordDocument):
    def __init__(self, tickets: TicketTemp, path_folder = None, path = "app/config/questions.docx"):
        super().__init__(path_folder, path)
        self.type_doc = "Вопросы"
        self.data = {
            'questions': tickets.export_question(),
            **tickets.configure.study
        }
