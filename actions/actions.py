from typing import Text, List, Dict, Any
from rasa_sdk import Tracker, Action,FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime

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
        
class ActionValidateRideForm(FormValidationAction):
    def name(self) -> Text:
        return "action_validate_ride_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Text]:
        return domain_slots

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(template="utter_confirm",
                                 departure=tracker.get_slot("departure"),
                                 arrival=tracker.get_slot("arrival"),
                                 time=tracker.get_slot("time"),
                                 date=tracker.get_slot("date") or "")
        return []

    def validate_time(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        # Walidacja i parsowanie czasu
        try:
            datetime.strptime(value, "%H:%M")
            return {"time": value}
        except ValueError:
            dispatcher.utter_message("Nieprawidłowy format czasu. Podaj godzinę w formacie HH:MM")
            return {"time": None}

    def extract_datetime(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        entities = tracker.latest_message.get("entities", [])
        datetime_entity = next((e for e in entities if e["entity"] == "datetime"), None)
        
        if datetime_entity:
            dt = datetime.fromisoformat(datetime_entity["value"])
            return {
                "time": dt.strftime("%H:%M"),
                "date": dt.strftime("%Y-%m-%d")
            }
        return {}