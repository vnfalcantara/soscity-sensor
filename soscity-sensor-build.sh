echo Copying file
sudo cp ~/Workspace/soscity-sensor/soscity-sensor.py /etc/init.d/;

echo Setting permission
sudo chmod +x /etc/init.d/soscity-sensor.py;

echo Updating update-rc.d
sudo update-rc.d soscity-sensor.py defaults;

echo OK!