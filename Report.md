## 2024 Mini Project Report

### Author: Jake Lee, Rohan Alexander

## Exercise 01

### Description:

Circuit connected as described in the problem. To find minimum brightness, we covered the photocell from all angles. To find maximum brightness we flashed a flashlight directly onto the photocell.

### Questions:

We discovered the dark reading to be around 430, therefore we set the variable to 400 to account for lower brightness.
The bright reading was between 47200 and 47500, so we set max_bright to be 50000, since light can be brighter than a phone flashlight.

### Images and Videos

https://github.com/user-attachments/assets/30a384e0-07f8-4b28-8e51-1a9d654865e9



## Exercise 02

### Description:

We connected the speaker as described in the problem. After playing around with the playtone function, we discovered we can play a song by storing the frequency orders in an array, and looping through each frequency in order. For the duration, we have a separate array that stores the number of beats each note is played for. In the loop each value in the duration array was adjusted to account for tempo.

### Questions:

We decided to play the Nokia theme. Since I already knew the notes of the song, I matched each note to its respective frequency and stored it in the frequency array.
<img width="502" alt="Screenshot 2024-09-17 at 4 46 21 PM" src="https://github.com/user-attachments/assets/a0e2d8c4-f411-4a39-b891-8ebebd712560">

The duration of the notes were stored in another array where 8 is a quarter note, 16 is a half note, and 32 is a whole note.
<img width="387" alt="Screenshot 2024-09-17 at 4 46 43 PM" src="https://github.com/user-attachments/assets/941a3939-7bb3-4116-bc2e-d5d493442eb4">

In the loop, each note and duration was played in order to create the Nokia theme.
<img width="545" alt="Screenshot 2024-09-17 at 4 46 58 PM" src="https://github.com/user-attachments/assets/45db2d3d-652f-4bab-a444-dcdac8652fb1">

### Images and Videos

https://github.com/user-attachments/assets/122957ca-1a90-4ee4-ab08-07880c59c463



## Exercise 03

### Description:

The goal of excercise 3 was to edit the provided game code to change to compute the minimum, maximum, and average response time of the player. Then we wanted to upload this data to firebase in a realtime database so we can keep record of all of the game attempts

### Main Approach:

For the calculation of the game code to compute the minimum, maximum, and average response time of the player, I added some code to the scorer that checks all of the succesful clicks of the button and measures if it is a new minimum or maximum response time. Then, after all of the 10 LED flashes I take all of the times and calculate the average over the 10 button click response times

```python
if t_good:
    min_time = min(t_good)
    max_time = max(t_good)
    avg_time = sum(t_good) / len(t_good)

    print(f"Min response time: {min_time} ms")
    print(f"Max response time: {max_time} ms")
    print(f"Avg response time: {avg_time:.2f} ms")

print(t_good)
```

After calculating the data we want to upload to our realtime firebase database, we concatenate it into a single dictionary and make a POST request to write the data to firebase

```python
 data = {
        "min": min_time,
        "max": max_time,
        "avg": avg_time,
    }
```

```python
def upload_data(data: dict) -> None:
    urequests.post(data_url + ".json", json=data)
```

### Images and Videos

![Firebase Dashboard](<doc/Screenshot 2024-09-17 at 5.02.10 PM.png>)

<p align="center">
<i>Firebase Dashboar</i>
</p>

[![Game Demo Video](<doc/Screenshot 2024-09-17 at 5.07.37 PM.png>)](https://drive.google.com/file/d/19pE2DpucMmSW0dcTH95ngYru_0Y3M-rb/view?usp=sharing)

<p align="center">
<i>Excersice 3 Demo Video</i>
</p>
