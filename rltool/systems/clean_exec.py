with open('exec.txt', 'r') as f:
  d = f.read()

states = [x[x.find("{"):x.find("}")+1].replace("\n","").replace("     ", " ").replace("   ", " ").replace("  ", " ").replace("<","\n<").replace("}", "\n}").replace(" ps", "ps").replace("{","\n{") for x in d.split("result State: ")]
print("\n".join(states))