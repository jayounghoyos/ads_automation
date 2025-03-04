// main.js

const selectedVacancies = [];

// Obtener el token CSRF del meta tag
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

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

        if (selectedVacancies.some(v => v.id === vacancyId)) {
            alert(`The vacancy with ID "${vacancyId}" has already been added.`);
            return;
        }

        if (!jobData[vacancyId]) {
            alert(`The ID "${vacancyId}" is not valid. Try another ID.`);
            return;
        }

        const jobTitle = jobData[vacancyId];
        selectedVacancies.push({ id: vacancyId, title: jobTitle });
    });

    renderVacancyList();
    input.value = '';
}

function renderVacancyList() {
    const list = document.getElementById('vacancyList');
    list.innerHTML = '';

    selectedVacancies.forEach((vacancy, index) => {
        const li = document.createElement('li');
        li.innerHTML = `Vacancy ID: ${vacancy.id} <br> Job Title: ${vacancy.title}`;

        const removeButton = document.createElement('button');
        removeButton.textContent = 'Remove';
        removeButton.onclick = () => {
            selectedVacancies.splice(index, 1);
            renderVacancyList();
        };

        li.appendChild(removeButton);
        list.appendChild(li);
    });
}

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
            alert('Vacancies have been published successfully!');
        } else {
            alert('Failed to publish vacancies.');
        }
    })
    .catch(error => {
        console.error('Error publishing vacancies:', error);
    });
}
