// main.js

const selectedVacancies = [];

function addVacancy() {
    const input = document.getElementById('vacancyInput');
    const vacancyId = input.value.trim();

    if (!vacancyId) {
        alert('Por favor, ingresa un ID de vacante.');
        return;
    }

    if (isNaN(vacancyId) || parseInt(vacancyId) <= 0) {
        alert('El ID de la vacante debe ser un número positivo.');
        return;
    }

    if (selectedVacancies.some(v => v.id === vacancyId)) {
        alert('Esta vacante ya ha sido agregada.');
        return;
    }

    if (!jobData[vacancyId]) {
        alert('El ID de la vacante no es válido. Intenta con otro ID.');
        return;
    }

    const jobTitle = jobData[vacancyId];
    selectedVacancies.push({ id: vacancyId, title: jobTitle });
    renderVacancyList();
    input.value = '';
}

function renderVacancyList() {
    const list = document.getElementById('vacancyList');
    list.innerHTML = '';

    selectedVacancies.forEach((vacancy, index) => {
        const li = document.createElement('li');
        li.innerHTML = `Vacante ID: ${vacancy.id} <br> Job Title: ${vacancy.title}`;

        const removeButton = document.createElement('button');
        removeButton.textContent = 'Eliminar';
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
        alert('No hay vacantes seleccionadas para automatizar.');
        return;
    }
    alert(`Automatizando la publicación de ${selectedVacancies.length} vacante(s)`);
}
