from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime

class ActionSearchConnection(Action):
    def name(self) -> Text:
        return "action_search_connection"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        departure = tracker.get_slot("departure_station")
        arrival = tracker.get_slot("arrival_station")
        date = tracker.get_slot("date") or datetime.today().strftime('%Y-%m-%d')
        time = tracker.get_slot("time") or datetime.today().strftime('%H:%M:%S')

        if not departure:
            dispatcher.utter_message(response="utter_ask_departure_station")
            return []
        
        if not arrival:
            dispatcher.utter_message(response="utter_ask_arrival_station")
            return []
        
        if not date:
            dispatcher.utter_message(response="utter_ask_date")
            return []
        
        if not time:
            dispatcher.utter_message(response="utter_ask_time")
            return []

        # Tutaj można dodać logikę wyszukiwania połączenia
        # W tym przykładzie po prostu wyświetlamy zebrane informacje
        
        dispatcher.utter_message(response="utter_offer_results",
            departure_station=departure,
            arrival_station=arrival,
            date=date,
            time=time)
        
        dispatcher.utter_message(response="utter_ask_buy_ticket")
        
        return []