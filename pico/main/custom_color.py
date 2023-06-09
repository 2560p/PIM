def main():
    machine_process_status = "IN_PROGRESS"  # Initial machine process status
    
    while True:
        if machine_process_status == "IN_PROGRESS":
            color = "yellow"
        elif machine_process_status == "COMPLETED":
            color = "Green"
        else:
            color = "skyblue"
        
        # Display the current color
        turn_off_rgb()
        print(f"Displaying Color: {color}")
        red, green, blue = colors[color]
        pwms[RED].duty_u16(map_range(red, 0, 255, 0, 65535))
        pwms[GREEN].duty_u16(map_range(green, 0, 255, 0, 65535))
        pwms[BLUE].duty_u16(map_range(blue, 0, 255, 0, 65535))
        
        time.sleep(2)
        
        # Update the machine process status (for demonstration purposes)
        if machine_process_status == "IN_PROGRESS":
            machine_process_status = "COMPLETED"
        else:
            machine_process_status = "IN_PROGRESS"
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        deinit_pwm_pins()