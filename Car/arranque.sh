cd /home/pi/.virtualenvs/cv 
echo $?
. bin/activate
echo $?
cd /home/pi/Desktop/smartCar-master/Car/
echo $?
python pruebaThreads.py --cascade haarcascade_frontalface_default.xml -p shape_predictor_68_face_landmarks.dat
echo $?
