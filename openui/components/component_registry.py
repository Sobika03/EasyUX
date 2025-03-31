from base_component import BaseComponent
from component_registry import register  # assuming the registry code is in `registry.py`
 
 
@register("button")
class ButtonComponent(BaseComponent):
    name = "button"
    template_path = "openui/components/Button/template.html"
    css_path = "openui/components/Button/style.css"
    js_path = "openui/components/Button/script.js"
 
    props = {
        "label": "Click Me",
        "color": "primary",   # Bootstrap-style: primary, danger, etc.
        "size": "md",         # sm, md, lg 
        "type": "button",     # submit, reset, button
        "icon": None,
        "id": "",
        "class": "", 
        "onclick": "",    }
 
    @property
    def class_hash(self):
        # You could use something more robust like hash(inspect.getsource(self.__class__))
        return hash(self.__class__.__name__)
 
    def get_context_data(self):
        return {
            "props": self.attributes,
            "slots": self.slots,
        }
 
    def before_render(self):
        classes = [
            "openui-btn",
            f"openui-btn-{self.attributes.get('color', 'primary')}",
            f"openui-btn-{self.attributes.get('size', 'md')}",
            self.attributes.get("class", "")
        ]
        self.attributes["class"] = " ".join(filter(None, classes))
        if self.attributes.get("onclick"):
            self.attributes["x-on:click"] = self.attributes["onclick"]