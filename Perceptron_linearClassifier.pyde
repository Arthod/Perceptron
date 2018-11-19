def setup():
    size(400, 400)
    global data_class0, data_class1, checking
    data_class0 = []
    data_class1 = []
    #Import 10 of both classes
    checking = 0
    if (True):
        #Class 0
        for i in range(10):
            data_class0.append([])
            img = loadImage('test_data/letters/class0/' + str(i) + '.png')
            img.loadPixels()
            pixel_count = []
            for n,p in enumerate(img.pixels):
                pixel_count.append((brightness(p)/255.0) - 0.5)
            x = 0
            for j in range(10):
                data_class0[i].append([])
                for k in range(10):
                    data_class0[i][j].append(pixel_count[x])
                    x += 1
                
        #Class 1
        for i in range(10):
            data_class1.append([])
            img = loadImage('test_data/letters/class1/' + str(i) + '.png')
            img.loadPixels()
            pixel_count = []
            for n,p in enumerate(img.pixels):
                pixel_count.append((brightness(p)/255.0) - 0.5)
            x = 0
            for j in range(10):
                data_class1[i].append([])
                for k in range(10):
                    data_class1[i][j].append(pixel_count[x])
                    x += 1
                    
    else:
        for i in range(10):
            data_class0.append([])
            data_class1.append([])
            for j in range(10):
                data_class0[i].append([])
                data_class1[i].append([])
                for k in range(10):
                    data_class0[i][j].append(random(-50, 50)/50.0)
                    data_class1[i][j].append(random(-50, 50)/50.0)
        
    global weight, bias        
    #Weight, bias
    bias = 1
    weight = []
    for i in range(10):
        weight.append([])
        for j in range(10):
            #weight[i].append(random(-50, 50)/50.0)
            weight[i].append(0)
                                
    global cellSize, learning_rate
    cellSize = 3
    learning_rate = 0.1
    
    #test input init
    global test_input
    test_input = []
    for i in range(10):
        test_input.append([])
        for j in range(10):
            test_input[i].append(0.5)
    print test_input
    
    
def draw():
    background(200)
    fill(0)
    text("class -1 from dataset", 20, 20)
    for i in range(len(data_class0)):
        classified = 0
        if forward_propagation(data_class0[i]) == -1:
            classified = 1
        draw_weight(i * (cellSize * 10 + 4) + 20, 30, data_class0[i], classified, cellSize)
    fill(0)
    text("class +1 from dataset", 20, 90)
    for i in range(len(data_class1)):
        classified = 0
        if forward_propagation(data_class1[i]) == 1:
            classified = 1
        draw_weight(i * (cellSize * 10 + 4) + 20, 100, data_class1[i], classified, cellSize)
    fill(0)
    text("weight vector", 20, 160)
    draw_weight(20, 170, weight, 1, cellSize * 4)
    
    fill(0)
    text("test input", 235, 160)
    draw_weight(235, 170, test_input, 1, cellSize * 4)
    fill(0)
    text("test prediction: " + str(forward_propagation(test_input)), 235, 325)
    
    if 235 + cellSize * 4 * 10 > mouseX > 235 and 170 + cellSize * 4 * 10 > mouseY > 170 and mousePressed:
        mx = (mouseX - 235) / (cellSize * 4)
        my = (mouseY - 170 - cellSize * 4) / (cellSize * 4)
        if mouseButton == LEFT:
            test_input[my][mx] = 0.5
        else:
            test_input[my][mx] = -0.5
    
    
    if frameCount%10 == 0:
        tick()
        
    
    
    
def tick():
    global checking
    backward_propagation(data_class0[checking], -1)
    backward_propagation(data_class1[checking], 1)

    checking += 1
    if checking == 9:
        checking = 0
    
def backward_propagation(input, desired_output):
    actual_output = forward_propagation(input)
    if (actual_output == desired_output):
        pass
        #print("Correctly classified")
        #Means its classified correctly.
    else:
        #It classified the input wrongly, update weights.
        print("Misclassified")
        for i in range(len(weight)):
            for j in range(len(weight[i])):
                weight[i][j] += input[i][j] * (desired_output - actual_output) * learning_rate
    
def forward_propagation(input):
    input_arr = []
    for i in range(len(input)):
        for j in range(len(input[i])):
            input_arr.append(input[i][j])
    weight_arr = []
    for i in range(len(weight)):
        for j in range(len(weight[i])):
            weight_arr.append(weight[i][j])
    sum = 0 + bias
    for i in range(len(weight_arr)):
        sum += weight_arr[i] * input_arr[i]
    return sign(sum)

    
def draw_weight(x, y, arr, classified, size): #classified (1 or 0, depending if weights classified it correctly or not.)
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            pushMatrix()
            fill((arr[i][j]+0.5) * 255)
            rect(j * size + x , i * size + y + size, size, size)
            if classified == 0:
                fill(255, 0, 0)
                rect(x + i * size, y, 5, 3) 
            popMatrix()
            
def sign(n):
    if n >= 0:
        return 1
    else:
        return -1 
