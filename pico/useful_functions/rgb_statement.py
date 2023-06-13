# main function for RGB LED lights
def main():
    color = "RED"  # Initial color
    
    while True:
        # Display the current color
        if color == "RED":
            pwms[RED].duty_u16(65535)  # Value of intensity
            pwms[GREEN].duty_u16(0)
            pwms[BLUE].duty_u16(0)
        elif color == "GREEN":
            pwms[RED].duty_u16(0)
            pwms[GREEN].duty_u16(65535)
            pwms[BLUE].duty_u16(0)
        elif color == "BLUE":
            pwms[RED].duty_u16(0)
            pwms[GREEN].duty_u16(0)
            pwms[BLUE].duty_u16(65535)
        
        time.sleep(1)
        
        # Update the color based on the machine process
        if machine_process_completed():
            color = "GREEN"
        elif machine_process_in_progress():
            color = "BLUE"
        else:
            color = "RED"
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        deinit_pwm_pins()