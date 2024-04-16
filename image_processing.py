from byuimage import Image
import sys


def validate_commands(args):
    flag = args[1]
    if ((flag in ['-d'] and len(args) > 1) or
            (flag in ['-s', '-g', '-f', '-m'] and len(args) > 2) or
            (flag in ['-k'] and len(args) > 3) or
            (flag in ['-y'] and len(args) > 6) or
            (flag in ['-b', '-c'] and len(args) > 7)):
        return True


def darken(input_file, output_file, percent):
    output_image = Image(input_file)
    for y in range(output_image.height):
        for x in range(output_image.width):
            pixel = output_image.get_pixel(x, y)
            pixel.red *= 1 - percent
            pixel.blue *= 1 - percent
            pixel.green *= 1 - percent
    output_image.save(output_file)


def sepia(input_file, output_file):
    output_image = Image(input_file)
    for y in range(output_image.height):
        for x in range(output_image.width):
            pixel = output_image.get_pixel(x, y)
            true_red = 0.393 * pixel.red + 0.769 * pixel.green + 0.189 * pixel.blue
            true_green = 0.349 * pixel.red + 0.686 * pixel.green + 0.168 * pixel.blue
            true_blue = 0.272 * pixel.red + 0.534 * pixel.green + 0.131 * pixel.blue
            pixel.red = true_red
            pixel.blue = true_blue
            pixel.green = true_green

            if pixel.red > 255:
                pixel.red = 255
            if pixel.blue > 255:
                pixel.blue = 255
            if pixel.green > 255:
                pixel.green = 255
    output_image.save(output_file)


def grayscale(input_file, output_file):
    output_image = Image(input_file)
    for y in range(output_image.height):
        for x in range(output_image.width):
            pixel = output_image.get_pixel(x, y)
            average_value = (pixel.red + pixel.green + pixel.blue) / 3
            pixel.red = average_value
            pixel.blue = average_value
            pixel.green = average_value
    output_image.save(output_file)


def make_borders(input_file, output_file, thickness, red, green, blue):
    old_image = Image(input_file)
    new_image = Image.blank(old_image.width + (thickness * 2), old_image.height + (thickness * 2))
    for pixel in new_image:
        pixel.blue = blue
        pixel.red = red
        pixel.green = green

    for y in range(thickness, new_image.height - thickness):
        for x in range(thickness, new_image.width - thickness):
            new_pixel = new_image.get_pixel(x, y)
            old_pixel = old_image.get_pixel(x - thickness, y - thickness)

            new_pixel.red = old_pixel.red
            new_pixel.blue = old_pixel.blue
            new_pixel.green = old_pixel.green
    new_image.save(output_file)


def flipped(input_file, output_file):
    """flips an image vertically"""
    og_image = Image(input_file)
    new_image = Image.blank(og_image.width, og_image.height)
    for y in range(0, og_image.height):
        for x in range(0, og_image.width):
            og_pixel = og_image.get_pixel(x, y)
            new_pixel = new_image.get_pixel(x, new_image.height - y - 1)
            new_pixel.blue = og_pixel.blue
            new_pixel.red = og_pixel.red
            new_pixel.green = og_pixel.green
    new_image.save(output_file)


def mirrored(input_file, output_file):
    """flips an image horizontally"""
    og_image = Image(input_file)
    new_image = Image.blank(og_image.width, og_image.height)
    for y in range(0, og_image.height):
        for x in range(0, og_image.width):
            og_pixel = og_image.get_pixel(x, y)
            new_pixel = new_image.get_pixel(new_image.width - x - 1, y)
            new_pixel.blue = og_pixel.blue
            new_pixel.red = og_pixel.red
            new_pixel.green = og_pixel.green
    new_image.save(output_file)


def collage(image1, image2, image3, image4, output_file, thickness):
    first_image = Image(image1)
    second_image = Image(image2)
    third_image = Image(image3)
    fourth_image = Image(image4)
    new_image = Image.blank(first_image.width + second_image.width + (thickness * 3),
                            first_image.height + third_image.height + (thickness * 3))
    for pixel in new_image:
        pixel.blue = 0
        pixel.red = 0
        pixel.green = 0

    for y in range(0, new_image.height):
        for x in range(0, new_image.width):
            new_pixel = new_image.get_pixel(x, y)
            if y in range(thickness, thickness + first_image.height):
                if x in range(thickness, thickness + first_image.width):
                    first_pixel = first_image.get_pixel(x - thickness, y - thickness)
                    new_pixel.red = first_pixel.red
                    new_pixel.blue = first_pixel.blue
                    new_pixel.green = first_pixel.green
                elif x in range((thickness * 2) + first_image.width, new_image.width - thickness):
                    second_pixel = second_image.get_pixel(x - (thickness * 2) - first_image.width, y - thickness)
                    new_pixel.red = second_pixel.red
                    new_pixel.blue = second_pixel.blue
                    new_pixel.green = second_pixel.green
            elif y in range((thickness * 2) + first_image.height, new_image.height - thickness):
                if x in range(thickness, thickness + third_image.width):
                    third_pixel = third_image.get_pixel(x - thickness, y - (thickness * 2) - first_image.height)
                    new_pixel.red = third_pixel.red
                    new_pixel.blue = third_pixel.blue
                    new_pixel.green = third_pixel.green
                elif x in range((thickness * 2) + first_image.width, new_image.width - thickness):
                    fourth_pixel = fourth_image.get_pixel(x - (thickness * 2) - third_image.width,
                                                          y - (thickness * 2) - second_image.height)
                    new_pixel.red = fourth_pixel.red
                    new_pixel.blue = fourth_pixel.blue
                    new_pixel.green = fourth_pixel.green
    new_image.save(output_file)


def detect_green(pixel, threshold, factor):
    average = (pixel.red + pixel.green + pixel.blue)/3
    if pixel.green >= factor * average and pixel.green > threshold:
        return True
    return False


def green_screen(foreground_image, background_image, output_file, threshold, factor):
    og_image = Image(foreground_image)
    back_image = Image(background_image)
    final_image = Image.blank(og_image.width, og_image.height)
    for y in range(0, og_image.height):
        for x in range(0, og_image.width):
            og_pixel = og_image.get_pixel(x, y)
            back_pixel = back_image.get_pixel(x, y)
            final_pixel = final_image.get_pixel(x, y)
            if not detect_green(og_pixel, threshold, factor):
                final_pixel.blue = og_pixel.blue
                final_pixel.red = og_pixel.red
                final_pixel.green = og_pixel.green
            else:
                final_pixel.blue = back_pixel.blue
                final_pixel.red = back_pixel.red
                final_pixel.green = back_pixel.green
    final_image.save(output_file)


def main(args):
    flag = args[1]
    if validate_commands(args):
        if flag == '-d':
            Image(args[2]).show()
        elif flag == '-k':
            darken(args[2], args[3], float(args[4]))
        elif flag == '-s':
            sepia(args[2], args[3])
        elif flag == '-g':
            grayscale(args[2], args[3])
        elif flag == '-b':
            make_borders(args[2], args[3], int(args[4]), args[5], args[6], args[7])
        elif flag == '-f':
            flipped(args[2], args[3])
        elif flag == '-m':
            mirrored(args[2], args[3])
        elif flag == '-c':
            collage(args[2], args[3], args[4], args[5], args[6], int(args[7]))
        elif flag == '-y':
            green_screen(args[2], args[3], args[4], int(args[5]), float(args[6]))


if __name__ == "__main__":
    main(sys.argv)
