FT_PRINTF_PATH = ../ft_printf

CC = gcc
CCFLAGS = -Wall -Wextra -Wno-format -g
LDFLAGS = -L$(FT_PRINTF_PATH) -lftprintf

NAME = ft_printf_test
PYTHON = python3
RM = rm -f
MAKE = make -j4

SRC = main.c helper.c tests/pft_tests.c tests/moulitest_tests.c
OBJ = $(SRC:.c=.o)

run: run_pretty

run_pretty: all
	./$(NAME) | $(PYTHON) prettier.py

run_pretty_verbose:
	./$(NAME) | $(PYTHON) prettier.py --verbose

run_pretty_quiet:
	./$(NAME) | $(PYTHON) prettier.py --quiet

run_raw: all
	./$(NAME)

all: $(NAME)

$(NAME): ft_printf_all clean $(OBJ)
	$(CC) $(LDFLAGS) $(CCFLAGS) -o $@ $(OBJ)

%.o: %.c
	$(CC) $(CCFLAGS) -c -o $@ $<

clean:
	$(RM) $(OBJ)

fclean: clean
	$(RM) $(NAME)

re: fclean all

ft_printf_all:
	$(MAKE) -C $(FT_PRINTF_PATH) all
