<!-- Navbar -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
        <!-- Landing page -->
        <a class="navbar-brand" href="{% url 'core:landing' %}">Droom</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
            aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                {% if request.session.company_id %}
                    <!-- User is logged in with company_id -->
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'core:dashboard' %}">Dashboard</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'core:manage_tables' %}">Manage Tables</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'users:logout' %}">Logout</a>
                    </li>
                {% else %}
                    <!-- User not logged in -->
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'users:login' %}">Login</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'users:register' %}">Register</a>
                    </li>
                {% endif %}
            </ul>
        </div>
    </div>
</nav>
<div class="container mt-2">
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        {% endfor %}
    {% endif %}
</div>
