'''
Created on 19-08-2014

@author: Marcial Hernandez Sanchez
'''
try:
    import xml.etree.ElementTree as ET
except ImportError:
    try:
        from elementtree.ElementTree import *
        import elementtree.ElementTree as ET
    except ImportError:
        raise ImportError('Cannot find any version of ElementTree')
 
assessmentItem  = ET.Element("assessmentItem", identifier="choiceMultiple", title="Titulo pregunta", adaptive="False", timeDependent="False", assessmentID="1")
comentarioAssessmentItem = ET.Comment("Nodo raiz pregunta, codigo debe ser dinamico")
assessmentItem.append(comentarioAssessmentItem)
assessmentItem.text = assessmentItem.get("title")

responseDeclaration = ET.SubElement(assessmentItem, "responseDeclaration", identifier="RESPONSE" , cardinality="single" , baseType="bloomComplexity", choiceQuantity="5")
comentarioResponseDeclaration = ET.Comment("Atributos alternativa pregunta")
responseDeclaration.append(comentarioResponseDeclaration)
#cantidadAlternativas=responseDeclaration.get("choiceQuantity")
#print(cantidadAlternativas)

correctResponse = ET.SubElement(responseDeclaration, "correctResponse")
comentarioCorrectResponse = ET.Comment("Alternativa correcta")
correctResponse.append(comentarioCorrectResponse)

valueCorrectResponse = ET.SubElement(correctResponse, "value")
comentarioValue = ET.Comment("Valor Alternativa correcta")
valueCorrectResponse.append(comentarioValue)
valueCorrectResponse.text = "Correct Choise"

outcomeDeclaration = ET.SubElement(assessmentItem,"outcomeDeclaration", identifier="SCORE", cardinality="single", baseType="float")
comentarioOutcomeDeclaration = ET.Comment("Valores que retorna al elegir alternativa")
outcomeDeclaration.append(comentarioOutcomeDeclaration)

defaultValue = ET.SubElement( outcomeDeclaration, "defaultValue")
comentarioDefaultValue = ET.Comment("Valor por defecto")
defaultValue.append(comentarioDefaultValue)

valueDefaultScore = ET.SubElement( defaultValue, "value", quantity="0")
comentarioValueDefaultValue = ET.Comment("Valor por defecto puntaje obtenido")
valueDefaultScore.append(comentarioValueDefaultValue)

itemBody = ET.SubElement(assessmentItem, "itemBody")
comentarioItemBody = ET.Comment("Cuerpo de la pregunta")
itemBody.append(comentarioItemBody)

statement = ET.SubElement(itemBody, "statement")
comentarioStatement = ET.Comment("Aqui falta analizar morfologia enunciado")
statement.append(comentarioStatement)
statement.text = "Enunciado"

choiceInteraction = ET.SubElement(itemBody,"choiceInteraction", responseIdentifier="RESPONSE", shuffle="True", maxChoices="1")
comentarioChoiceInteraction = ET.Comment("Inicio y propiedades pregunta")
choiceInteraction.append(comentarioChoiceInteraction)

prompt = ET.SubElement(choiceInteraction, "prompt")
comentarioPrompt = ET.Comment("Pregunta, Aqui falta analizar morfologia pregunta")
prompt.append(comentarioPrompt)
prompt.text = "Pregunta"

simpleChoice = [ET.SubElement(prompt,"simpleChoice", num=str(i)) for i in xrange(int(responseDeclaration.get("choiceQuantity")))]
respuestas=["A", "B", "C", "D", "E"]

cantidadElementos=len(simpleChoice)
contador=0
for alternativa in simpleChoice:
    contador=contador+1
    letraAlternativa = chr(64+contador)+ chr(41)+" "
    alternativa.text = letraAlternativa+respuestas[0]
    respuestas.pop(0)
    if (contador==cantidadElementos):
        comentarioSimpleChoice = ET.Comment("Solo la ultima alternativa lleva comentario")
        alternativa.append(comentarioSimpleChoice)

tree = ET.ElementTree(assessmentItem )
tree.write("filename.xml", xml_declaration=True, encoding='utf-8', method="xml")