import re


def checkToken(layer, token):
    token = re.sub('[,]', "", token)
    result = []
    prefix = "  " * layer

    if ("\"" in token):
        result.append(prefix + "type: string")
        layer -= 1
    elif ("{" in token):
        result.append(prefix + "type: object")
        result.append(prefix + "properties:")
        layer += 1
    elif ("[" in token):
        result.append(prefix + "type: array")
        result.append(prefix + "items:")
        layer += 1
    elif (token in ["true", "false"]):
        result.append(prefix + "type: boolean")
        layer -= 1
    elif (']' in token or '}' in token):
        layer -= 1
        return None, layer
    else:
        result.append(prefix + "type: number")
        layer -= 1
    return result, layer


with open("./res.json", "r", encoding="utf-8") as f:
    data = f.read()
    data = re.sub("[ ]", "", data)
    data = data.split("\n")
    result = ["schema:"]
    layers = []
    layer = 1
    name = ""
    prefix = "            "

    for line in data:
        token = line.split(':')
        if(len(token) > 1):
            name = re.sub("[\"]", "", token[0])
            value = token[1]
            result.append("  " * layer + name + ":")
            layer += 1
            resultStr, resultLayer = checkToken(layer, token[1])
            if(resultStr is not None):
                result += resultStr
            layer = resultLayer
            if("{" in token[1]):
                layers.append(1)

        else:
            resultStr, resultLayer = checkToken(layer, token[0])
            if(resultStr is not None):
                result += resultStr
            layer = resultLayer
            if("{" in token[0]):
                layers.append(0)
            if("}" in token[0]):
                layer -= layers[-1]
                layers.pop()
    for line in result:
        print(prefix + line)
