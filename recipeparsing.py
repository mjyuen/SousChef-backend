import re

def parse(text):
  class Tagged:
    quantity = ""
    unit = ""
    comment = ""
    name = ""

  unitSet = ([ "pinch", "pinches" "dash", "dashes" "teaspoon", "teaspoons", "tsp", "tablespoon", "tablespoons", "tbsp", "can", "cans", "cup", "cups", "slices", "slice", "dollop", "dollops", "scoops", "scoops", "gram", "grams", "containers", "container", "packets", "packet", "slice", "slices", "liters", "liter", "pounds", "pound", "lbs", "bunch", "bunches", "lb", "sprigs", "sprig", "ounces", "oz", "ounce", "pints", "pint", "gallon", "gallons", "medium", "large", "small", "branch" ])

  #testInput = "1 pinch of salt"
  #testInput = "1 stick of butter"
  #testInput = "2 cups/255 grams all-purpose flour (preferably unbleached), plus more as needed"
  testInput = text
  testParen = "1 tbsp olive oil (vegetable also works)"

  ingredient = Tagged()
  ingredient1 = Tagged()

  # Text enclosed by parentheses is a comment
  parenMatch = re.search(r'\((.*?)\)', testInput)
  if parenMatch:
    ingredient.comment = parenMatch.group(1)
    testInput = re.sub(r'\((.*?)\)', '', testInput)

  print(ingredient.comment)

  # Text after comma is part of the comment
  commaSplit = testInput.split(',', 1)
  if len(commaSplit) == 2:
    ingredient.comment = commaSplit[1].lstrip()
    testInput = commaSplit[0]

  # Split text based on spaces
  splitTest = list(map(str.strip, testInput.split(' ')))
  print(splitTest)

  # Find unit of measurement based on vocabulary and regex if the text offers two measurements
  unitIndex = -1
  ind = 0
  for word in splitTest:
    foundAlternate = re.search("\/\d+", word)
    if foundAlternate:
      if splitTest[ind + 1] in unitSet:
        slashSplit = splitTest[ind].split('/', 1)
        splitTest[ind + 1] = ''
        splitTest[ind] = ''
        ingredient.unit = slashSplit[0]
        unitIndex = ind + 1
        print(word)
        print(unitIndex)
        print(splitTest)
    if word in unitSet:
      ingredient.unit = word
      unitIndex = ind
      if splitTest[ind + 1] == "of":
        splitTest[ind + 1] = ''
      print(word)
      print(unitIndex)
      break
    ind+=1

  # If unit is not in the vocab set but is something like 1 clove of garlic
  if unitIndex == -1:
    for i in range(1, len(splitTest) - 1):
      if splitTest[i] == "of":
        unitIndex = i - 1
        ingredient.unit = splitTest[i-1]
        splitTest[i] = ''
        break

  # Get quantity relative to unit, or if no unit, take the first integer
  # No integer, assume 1
  #print(splitTest)
  #print(unitIndex)
  quantity = ""
  if unitIndex > 0:
    for i in range(0, unitIndex):
      quantity = quantity + splitTest[i]
  else:
    if splitTest[0].isdigit():
      quantity = splitTest[0]
      unitIndex = 0
    else:
      quantity = 1
  ingredient.quantity = quantity    
  print(quantity)

  # Get comment about name
  commentIndex = unitIndex
  for i in range(unitIndex + 1, len(splitTest) - 1):
    word = splitTest[i]
    match = re.search(".*ly$", word)
    if match:
      ingredient.comment = match.string + " " + splitTest[i + 1]
      commentIndex = i + 1
      break
    match2 = re.search(".*ed$", word)
    if match2 and (word != "red"):
      ingredient.comment = match2.string
      commentIndex = i + 1
      break

  # Get name of ingredient
  for i in range(commentIndex + 1, len(splitTest)):
    ingredient.name = ingredient.name + " " + splitTest[i]
  ingredient.name = str.strip(ingredient.name)

  print("Unit: " + ingredient.unit)
  print("Quantity: " + ingredient.quantity)
  print("Comment: " + ingredient.comment)
  print("Name: " + ingredient.name)
  result = {"quantity": ingredient.quantity, "unit": ingredient.unit, "name": ingredient.name, "comment": ingredient.comment}
  
  return(result)

def main():
  print(parse("1 clove of garlic"))
  
if __name__== "__main__":
  main()