# melvec

A small vector library for python

---

### Installation:

To install this package type `pip install melvec` in a console/terminal.

### Usage:

To import the package in your code use: `import melvec`.  
To create a 2D-Vector use: `melvec.Vec2()`.  
To create a 3D-Vector use: `melvec.Vec3()`.

For easy access to the vector classes it is recommended import the classes directly with: `from melvec import Vec2, Vec3`.

#### Example code snippets:

##### Using `import melvec`:

    import melvec
                
    u = melvec.Vec2(10, 2)
    v = melvec.Vec2(3, 3)  
    w = u + v  # -> Vec(13, 5)

    print(u.dot(w))  # -> 140

##### Using `from melvec import Vec2, Vec3`:

    from melvec import Vec2, Vec3
                
    u = Vec2(10, 2)
    v = Vec2(3, 3)  
    w = u + v  # -> Vec(13, 5)

    print(u.dot(w))  # -> 140
