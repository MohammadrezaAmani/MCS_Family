# AUT INFO


According to the tradition at Amirkabir University of Technology and a beautiful custom within the Faculty of Mathematics and Computer Science, every year, students with a format similar to `year-faculty_code-student_code` are recognized as "parents" for incoming students with the same format. For example, I, with the student ID `9913004`, am the "parent" of Amirhossein with the student ID 40013004, who entered the university exactly one year after me. As his first friend and mentor, I am responsible for helping him with course selection and surviving the challenging university life.

Now, with this code, you can easily find your academic "parents" and see up to 20 generations above yourself.

### HOW TO USE?

Clone The repository and inter your information in `main.py` file and run it
for example:
``` python
user = AutInfo(
    username='9913004',
    password='1122334455'
)
```

For getting special User information just use `AutInfo.get(student_id)` function:

``` python
user.get(40013004)
```
output:
```python
>>> (40013004, 'امیرحسین آذرپور')
```
and for get special range of users just use `AutInfo.get_range(start, end)`

``` python
user.get_range(9913004,9913006)
```
output:
```python
>>> [
    ("40013004", "امیرحسین اذرپورحسن کیاده"),
    ("40013005", "سینا ارزبین"),
    ("40013006", "مبینا افشاری"),
    ("40013007", "مهدی باقریان"),
]
```