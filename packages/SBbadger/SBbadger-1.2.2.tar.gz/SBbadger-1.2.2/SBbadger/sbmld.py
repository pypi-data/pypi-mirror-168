
import SBMLDiagrams
import tellurium as te

# print(SBMLDiagrams.get_distribution("simplegist").version)

# df = SBMLDiagrams.load("models/sbmld10/sbml/sbmld10_2.sbml")
# df.autolayout()

for i in range(100):
    df = SBMLDiagrams.load("models/sbmld10/sbml/sbmld10_" + str(i) + ".sbml")
    df.autolayout()
    df.draw(output_fileName="models/sbmld10/auto/sbmld10_" + str(i) + ".png")
