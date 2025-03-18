# plik: actions/actions.py (Rasa Custom Actions)
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime

class ActionSearchConnections(Action):
    def name(self) -> Text:
        return "action_search_connections"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Przykładowe stałe dane połączeń
        static_connections = [
            {
                "departure_time": "08:15",
                "arrival_time": "11:30",
                "duration": "3h15m",
                "train_type": "EIP",
                "price": 120
            },
            {
                "departure_time": "09:45",
                "arrival_time": "13:00",
                "duration": "3h15m",
                "train_type": "TLK",
                "price": 80
            },
            {
                "departure_time": "12:00",
                "arrival_time": "15:30",
                "duration": "3h30m",
                "train_type": "IC",
                "price": 95
            }
        ]

        # Formatowanie wyników
        message = "Przykładowe połączenia (demo):\n\n"
        for i, conn in enumerate(static_connections, 1):
            message += (
                f"{i}. {conn['departure_time']} - {conn['arrival_time']} "
                f"(Czas podróży: {conn['duration']})\n"
                f"   Typ pociągu: {conn['train_type']}   Cena: {conn['price']} PLN\n\n"
            )

        dispatcher.utter_message(text=message)
        dispatcher.utter_message(response="utter_offer_ticket_purchase")
        
        return []

class ActionStartPurchase(Action):
    def name(self) -> Text:
        return "action_start_purchase"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Symulacja procesu zakupu
        dispatcher.utter_message(text="🔒 Przechodzisz do bezpiecznego procesu płatności...")
        dispatcher.utter_message(text="✅ Zarezerwowano bilet! Numer rezerwacji: PKP-123456")
        dispatcher.utter_message(text="Dokończ płatność na stronie PKP: https://www.pkpsa.pl")
        
        return []