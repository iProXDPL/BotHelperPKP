from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionShowWeather(Action):
    def name(self) -> Text:
        return "action_show_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Tutaj zwykle byłaby logika pobierająca dane pogodowe z API
        city = "Warszawa"  # Można dodać ekstrakcję miasta z encji
        temperature = "20°C"
        
        response = f"Aktualna pogoda w {city}: {temperature}, słonecznie 🌞"
        dispatcher.utter_message(text=response)
        
        return []