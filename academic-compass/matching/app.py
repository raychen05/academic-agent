
from matching.matcher import OrgMatcher

if __name__ == "__main__":
    matcher = OrgMatcher()
    while True:
        name = input("\nEnter organization name: ")
        result = matcher.match(name)
        print("→ Match:", result["match"])
        print("→ Canonical:", result["canonical"])
