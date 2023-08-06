
class DocTestDB:
    ROBOT_LISTENER_API_VERSION = 2
    def __init__(self):
        print("SampleListener initialized")
        self.current_test = None
        self.current_testid = None

    def start_test(self, name, attrs):
        self.current_test = name
        self.current_testid = None
        tags = attrs.get("tags", [])
        for tag in tags:
            if tag.startswith("test_id"):
                self.current_testid = tag.split("=")[1]
                break
        
    def end_keyword(self, name, attributes):
        if attributes['kwname'] == 'Compare Images':
            if attributes['status'] == 'FAIL':
                print(f"\n{attributes['kwname']}")
                print(f"\n{attributes['args']}")

    def log_message(self, message):
        import re
        if "img" in message["message"]:
            print(message["message"])
            # Get all href= attributes from the message
            hrefs = re.findall(r'href=[\'"]?([^\'" >]+)', message["message"])
            # Get all src= attributes from the message
            srcs = re.findall(r'src=[\'"]?([^\'" >]+)', message["message"])
            for link in hrefs:
                print(f"\nUploading {link} for test case {self.current_test}")
            