from pytest_nlcov import git


def test_get_new_lines_per_file(mocker):
    diff = r"""diff --git a/added_file.py b/added_file.py
new file mode 100644
index 0000000..9b710f3
--- /dev/null
+++ b/added_file.py
@@ -0,0 +1,4 @@
+This was missing!
+Adding it now.
+
+Only for testing purposes.
\ No newline at end of file
diff --git a/modified_file.py b/modified_file.py
index c7921f5..8946660 100644
--- a/modified_file.py
+++ b/modified_file.py
@@ -1,5 +1,7 @@
 This is the original content.

-This should be updated.
+This is now updated.
+
+This is a new line.

 This will stay.
\ No newline at end of file
diff --git a/modified_file b/modified_file
index c7921f5..8946660 100644
--- a/modified_file
+++ b/modified_file
@@ -1,5 +1,7 @@
 This is the original content.

-This should be updated.
+This is now updated.
+
+This is a new line.

 This will stay.
\ No newline at end of file
diff --git a/removed_file.py b/removed_file.py
deleted file mode 100644
index 1f38447..0000000
--- a/removed_file.py
+++ /dev/null
@@ -1,3 +0,0 @@
-This content shouldn't be here.
-
-This file will be removed.
\ No newline at end of file
"""
    mocker.patch("pytest_nlcov.git.get_diff", lambda _, __: diff)

    new_lines_per_file = git.get_new_lines_per_file(
        "master",
    )

    assert [str(i).split("/")[-1] for i in new_lines_per_file.keys()] == [
        "added_file.py",
        "modified_file.py",
        "modified_file",
    ]

    new_lines_per_file = git.get_new_lines_per_file("master", "*.py")

    assert [str(i).split("/")[-1] for i in new_lines_per_file.keys()] == [
        "added_file.py",
        "modified_file.py",
    ]

    assert [lineno for lines in new_lines_per_file.values() for lineno, _ in lines.items()] == [1, 2, 3, 4, 3, 4, 5]
    assert [lineno for lines in new_lines_per_file.values() for lineno, line in lines.items() if line.is_empty] == [
        3,
        4,
    ]
