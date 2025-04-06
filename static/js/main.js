const selectedVacancies = [];

// Obtener el token CSRF del meta tag
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// Añadir una vacante por ID
function addVacancy() {
    const input = document.getElementById('vacancyInput');
    const inputValues = input.value.trim();

    if (!inputValues) {
        alert('Please enter one or more vacancy IDs.');
        return;
    }

    const vacancyIds = inputValues.split(',').map(id => id.trim());

    vacancyIds.forEach(vacancyId => {
        if (isNaN(vacancyId) || parseInt(vacancyId) <= 0) {
            alert(`The ID "${vacancyId}" is not a valid positive number.`);
            return;
        }

        if (selectedVacancies.some(v => v.job_id === vacancyId)) {
            alert(`The vacancy with ID "${vacancyId}" has already been added.`);
            return;
        }

        if (!jobData[vacancyId]) {
            alert(`The ID "${vacancyId}" is not valid. Try another ID.`);
            return;
        }

        const jobTitle = jobData[vacancyId];
        selectedVacancies.push({ job_id: vacancyId, title: jobTitle });  // 👈 CAMBIO CORRECTO AQUÍ
    });

    renderVacancyList();
    input.value = '';
}

// Renderizar la lista en la interfaz
function renderVacancyList() {
    const list = document.getElementById('vacancyList');
    list.innerHTML = '';

    selectedVacancies.forEach((vacancy, index) => {
        const li = document.createElement('li');
        li.innerHTML = `
            <strong>Vacancy ID:</strong> ${vacancy.job_id}<br>
            <strong>Job Title:</strong> ${vacancy.title}
        `;

        const removeButton = document.createElement('button');
        removeButton.textContent = 'Remove';
        removeButton.classList.add('remove-button');
        removeButton.onclick = () => {
            selectedVacancies.splice(index, 1);
            renderVacancyList();
        };

        li.appendChild(removeButton);
        list.appendChild(li);
    });
}

// Automatizar la publicación de vacantes
function automatizar() {
    if (selectedVacancies.length === 0) {
        alert('No vacancies selected to automate.');
        return;
    }

    fetch('/publicar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ vacancies: selectedVacancies }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('✅ Vacancies have been published successfully!');
            selectedVacancies.length = 0;
            renderVacancyList();
        } else {
            alert('❌ Failed to publish vacancies.');
            console.error('Error:', data.error);
        }
    })
    .catch(error => {
        console.error('Error publishing vacancies:', error);
        alert('⚠️ Something went wrong while publishing.');
    });
}

// Permitir añadir vacantes presionando Enter
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('vacancyInput');
    input.addEventListener('keydown', event => {
        if (event.key === 'Enter') {
            event.preventDefault();
            addVacancy();
        }
    });
});
