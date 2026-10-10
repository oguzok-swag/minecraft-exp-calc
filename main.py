from flask import Flask, render_template, request
import time

app = Flask(__name__)


def xp_for_level(level):
    """Возвращает общее количество XP, необходимое для достижения уровня."""

    if level < 0:
        raise ValueError("Уровень не может быть отрицательным.")

    if level <= 16:
        return level ** 2 + 6 * level

    elif level <= 31:
        return int(2.5 * level ** 2 - 40.5 * level + 360)

    else:
        return int(4.5 * level ** 2 - 162.5 * level + 2220)


def xp_to_next_level(level):
    """Возвращает количество XP для перехода на следующий уровень."""

    if level < 0:
        raise ValueError("Уровень не может быть отрицательным.")

    if level <= 15:
        return 2 * level + 7

    elif level <= 30:
        return 5 * level - 38

    else:
        return 9 * level - 158


def xp_between_levels(current_level, target_level):
    """Возвращает количество XP между двумя уровнями."""

    if current_level < 0 or target_level < 0:
        raise ValueError("Уровень не может быть отрицательным.")

    if target_level <= current_level:
        raise ValueError(
            "Целевой уровень должен быть выше текущего."
        )

    current_xp = xp_for_level(current_level)
    target_xp = xp_for_level(target_level)

    return target_xp - current_xp


def level_from_xp(total_xp):
    """Определяет уровень по общему количеству XP."""

    if total_xp < 0:
        raise ValueError("XP не может быть отрицательным.")

    level = 0

    while xp_for_level(level + 1) <= total_xp:
        level += 1

    return level


def progress_in_level(total_xp):
    """Возвращает XP, накопленную внутри текущего уровня."""

    level = level_from_xp(total_xp)

    current_level_xp = xp_for_level(level)

    return total_xp - current_level_xp


@app.route("/", methods=["GET", "POST"])
def index():

    result = None
    error = None

    current_level = None
    target_level = None

    current_xp = None
    target_xp = None
    required_xp = None
    next_level_xp = None
    level_progress = None

    if request.method == "POST":

        time.sleep(10)

        try:
            current_level = int(request.form["current_level"])
            target_level = int(request.form["target_level"])

            if current_level < 0 or target_level < 0:
                raise ValueError(
                    "Уровни не могут быть отрицательными."
                )

            if target_level <= current_level:
                raise ValueError(
                    "Целевой уровень должен быть выше текущего."
                )

            current_xp = xp_for_level(current_level)
            target_xp = xp_for_level(target_level)

            required_xp = xp_between_levels(
                current_level,
                target_level
            )

            next_level_xp = xp_to_next_level(current_level)

            level_progress = progress_in_level(current_xp)

        except (ValueError, TypeError) as e:
            error = str(e)

    return render_template(
        "index.html",
        result=required_xp,
        error=error,
        current_level=current_level,
        target_level=target_level,
        current_xp=current_xp,
        target_xp=target_xp,
        next_level_xp=next_level_xp,
        level_progress=level_progress
    )


if __name__ == "__main__":
    app.run(debug=True)