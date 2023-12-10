from flask import Flask, jsonify
import random

def Onepercent():
    if random.random() < 0.01:
        return False
    else:
        return True
        
def gen_num(idealmin,idealmax,lowmin,lowmax,negchance):
    try:
        randomval = random.random()
        #pos
        if randomval < negchance:
            return random.randint(idealmin,idealmax)
        #neg
        else:
            return random.randint(lowmin,lowmax)
    except:
        print("error detected",idealmin,idealmax,lowmin,lowmax,negchance)
        return 0

def getNums():
    vals = []

    state = Onepercent()
    print("creating new values")
    if not state:
        temperature = 50
        p_output = 0
        usage = 0
        rad_level = gen_num(0, 5, 10, 10000, 0.95)
    else:
        temperature = gen_num(100, 400, 500, 5000, 0.95)
        
        p_output = gen_num(1600, 2000, 0, 1500, 0.95)
        
        usage = gen_num(90, 100, 0, 75, 0.90)
        
        rad_level = gen_num(0, 5, 10, 10000, 0.95)
    
    vals.append([temperature, rad_level, p_output, usage, state])
    
    return vals
    
app = Flask(__name__)
print("test")
@app.route('/random', methods=['GET'])
def get_values():
    values = getNums()
    print(values)
    return jsonify({'temperature': values[0][0],
                     'radiation_level': values[0][1],
                     'power_output': values[0][2],
                     'usage_capacity_percentage': values[0][3],
                     'state': values[0][4]
                     })

if __name__ == '__main__':
    app.run(debug=True)