import pygame
import serial
import time

applicationClose = False
serialStringIn = ""
newDataAvaialble = False
previous_time = time.time()
previous_data_index = 0
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 0, 255)
timeUnit = "us"
timeBase = 100

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('monospace', 12)
# Create main window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("ArduinoScope")

# Serial port setup
serialPort = serial.Serial('/dev/ttyACM1', 115200)


while not applicationClose:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            applicationClose = True
            serialPort.close()
            pygame.display.quit()
            pygame.quit()

    if serialPort.in_waiting > 0:
        serialStringIn = serialPort.readline().strip()
        if serialStringIn[-2:] == b'R?':
            serialPort.reset_input_buffer()
            serialPort.write(b'K')
            while serialPort.in_waiting < 99:
                time.sleep(0.00001)

            data = serialPort.read(100)
            newDataAvaialble = True
            serialPort.write(b'K')

            # Calculate frequency
            current_time = time.time()
            time_span = current_time - previous_time
            num_data_points = 99  # Assuming 99 data points
            if num_data_points > 0 and time_span > 0:
                frequency = 1 / (time_span / num_data_points)
            else:
                frequency = 0

            previous_time = current_time
            previous_data_index += 99

            # Calculate average voltage
            average = sum(data) / len(data)

            min_value = 0
            max_value = 255

            for i in range(0, 99):
                if data[i] > max_value:
                    max_value = data[i]
                if data[i] < min_value:
                    min_value = data[i]

                    
        serialPort.reset_input_buffer()


    if newDataAvaialble:
        screen.fill(BLACK)

        for i in range(0, 99):
            if i < 99:
                pygame.draw.line(screen, RED, [40 + (i * 4), 400 - data[i]], [40 + ((i + 1) * 4), 400 - data[i + 1]], 2)

        # Average line
        pygame.draw.line(screen, BLUE, [40, 400 - average], [500, 400 - average], 1)

        # Plot axis
        pygame.draw.line(screen, GREEN, [40, 400], [500, 400], 1)
        pygame.draw.line(screen, GREEN, [40, 400], [40, 145], 1)

        # Plot labels
        label_5V = myfont.render('5.0V', False, RED)
        label_3_3V = myfont.render('3.3V', False, RED)
        label_2_5V = myfont.render('2.5V', False, RED)
        label_0V = myfont.render('0.0V', False, RED)

        label_time0 = myfont.render('0' + timeUnit, False, WHITE)
        label_time25 = myfont.render(str(timeBase * 25) + timeUnit, False, WHITE)
        label_time50 = myfont.render(str(timeBase * 50) + timeUnit, False, WHITE)
        label_time75 = myfont.render(str(timeBase * 75) + timeUnit, False, WHITE)
        label_time100 = myfont.render(str(timeBase * 100) + timeUnit, False, WHITE)

        # Print frequency at the top of the GUI
        label_frequency = myfont.render("Frequency: {:.2f} Hz".format(frequency), False, WHITE)
        screen.blit(label_frequency, (10, 10))

        # Print average value and voltage line
        averageV = (average / 255) * 5
        averageV = round(averageV, 2)
        label_average = myfont.render(str(averageV) + 'V', False, BLUE)
        screen.blit(label_average, (510, 393 - average))

        # Print maximum/minimum values and voltage line
        minV = round((min_value / 255) * 5, 2)
        maxV = round((max_value / 255) * 5, 2)
        label_min = myfont.render(str(minV) + 'V', False, PINK)
        label_max = myfont.render(str(maxV) + 'V', False, WHITE)
        pygame.draw.line(screen, WHITE, [40, 400 - min_value], [500, 400 - min_value], 1)
        pygame.draw.line(screen, PINK, [40, 400 - max_value], [500, 400 - max_value], 1)
        screen.blit(label_min, (510, 393 - min_value))
        screen.blit(label_max, (510, 393 - max_value))

        # Print axis labels and time scales
        screen.blit(label_5V, (5, 138))
        screen.blit(label_3_3V, (5, 225))
        screen.blit(label_2_5V, (5, 266))
        screen.blit(label_0V, (5, 393))

        screen.blit(label_time0, (40, 410))
        screen.blit(label_time25, (40 + 80, 410))
        screen.blit(label_time50, (40 + 180, 410))
        screen.blit(label_time75, (40 + 280, 410))
        screen.blit(label_time100, (40 + 360, 410))

        newDataAvaialble = False
        pygame.display.flip()



