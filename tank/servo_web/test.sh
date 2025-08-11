#!/bin/bash
for chip in /sys/class/pwm/pwmchip*; do
  echo "Checking $chip ..."
  npwm=$(cat $chip/npwm)
  for i in $(seq 0 $((npwm-1))); do
    if [ ! -d $chip/pwm$i ]; then
      echo $i | sudo tee $chip/export
    fi
    echo 0 | sudo tee $chip/pwm$i/enable
    if echo 20000000 | sudo tee $chip/pwm$i/period; then
      echo 1500000 | sudo tee $chip/pwm$i/duty_cycle
      if echo 1 | sudo tee $chip/pwm$i/enable; then
        echo "  $chip/pwm$i SUCCESS (active)"
        echo 0 | sudo tee $chip/pwm$i/enable
      fi
    fi
  done
done
