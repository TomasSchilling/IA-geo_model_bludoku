import tensorflow as tf
from tensorflow.keras import layers, models
import os
import numpy as np
import automatic
import time

def create_model():
    model = models.Sequential()
    model.add(layers.Input(shape=(94,)))  
    model.add(layers.Dense(50, activation='relu')) 
    model.add(layers.Dense(81, activation='softmax'))  
    model.compile(optimizer='adam', loss='categorical_crossentropy')
    return model

def save_best_model(best_model, model_name='best_model.h5', generation_folder='Generaciones'):
    # Save in the same folder
    best_model.save(model_name)
    print(f"Model saved as {model_name}.")

    # Create the Generaciones folder if it doesn't exist
    if not os.path.exists(generation_folder):
        os.makedirs(generation_folder)
        print(f"Created folder: {generation_folder}")

    # Determine the next generation index
    generation_index = 1
    while True:
        gen_model_name = f"Mod gen {generation_index}.h5"
        gen_model_path = os.path.join(generation_folder, gen_model_name)

        if not os.path.isfile(gen_model_path):
            break  # Found a name that doesn't exist, we can use this
        generation_index += 1

    # Save the model in the Generaciones folder
    best_model.save(gen_model_path)
    print(f"Model saved as {gen_model_path}.")

def load_or_create_models(model_file='best_model.h5', num_models=100, modification_factor=0.0005):
    models_list = []
    
    # Check if the model file exists
    if os.path.isfile(model_file):
        print(f"Loading model from {model_file}...")
        best_model = models.load_model(model_file)
        models_list.append(best_model)
        for i in range(num_models-1):
            

            for layer in best_model.layers:
                if isinstance(layer, tf.keras.layers.Dense):
                    weights, biases = layer.get_weights()
                    weights += np.random.normal(0, modification_factor, weights.shape)  # Modify weights
                    biases += np.random.normal(0, modification_factor, biases.shape)    # Modify biases
                    layer.set_weights([weights, biases])  # Set the modified weights and biases
            models_list.append(best_model)
    else:
        print(f"{model_file} not found. Creating {num_models} new models...")
        for _ in range(num_models):
            models_list.append(create_model())

    return models_list

# Example usage
models_list = load_or_create_models()

Game_tester=automatic.Game()
total_games = 100
scores_list = []

i=0
for model in models_list:
    i+=1
    model_score=0
    
    for game_i in range(total_games):
        t1=time.time()
        Game_tester.reset_game()
        input_data = Game_tester.join_input()
        input_data = np.array(input_data).astype(int)
        input_data = input_data.reshape(1, -1)
        
        legal_move = True  # Flag to check if the last move was legal
          
        while legal_move ==True:
            # Get the model's action
            action = model.predict(input_data, verbose=0)  
            action_taken = np.argmax(action)  
            
    
            legal_move = Game_tester.play_number(action_taken)  
            if legal_move ==True:
                # Update the input for the next prediction
                input_data = Game_tester.join_input()
                input_data = np.array(input_data).astype(int)  
                input_data = input_data.reshape(1, -1)  
        model_score+=Game_tester.score
        print(time.time()-t1)

    scores_list.append(model_score)
    print(f" {i} = {Game_tester.score}")

model_to_save= scores_list.index(max(scores_list))

save_best_model(models_list[model_to_save])

print("modelo guardado")
print(scores_list,max(scores_list))