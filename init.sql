-- Создание таблицы деятельностей (activities) с древовидной структурой
CREATE TABLE IF NOT EXISTS activities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    parent_id INTEGER REFERENCES activities(id) ON DELETE SET NULL,
    level INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы зданий (buildings)
CREATE TABLE IF NOT EXISTS buildings (
    id SERIAL PRIMARY KEY,
    address VARCHAR(500) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы организаций (organizations)
CREATE TABLE IF NOT EXISTS organizations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    building_id INTEGER NOT NULL REFERENCES buildings(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы для телефонов организаций (один ко многим)
CREATE TABLE IF NOT EXISTS organization_phones (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    phone_number VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы связи организаций и деятельностей (многие ко многим)
CREATE TABLE IF NOT EXISTS organization_activities (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    activity_id INTEGER NOT NULL REFERENCES activities(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(organization_id, activity_id)
);

-- Создание индексов для оптимизации запросов
CREATE INDEX IF NOT EXISTS idx_activities_parent_id ON activities(parent_id);
CREATE INDEX IF NOT EXISTS idx_activities_level ON activities(level);
CREATE INDEX IF NOT EXISTS idx_buildings_coordinates ON buildings(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_organizations_building_id ON organizations(building_id);
CREATE INDEX IF NOT EXISTS idx_organizations_name ON organizations(name);
CREATE INDEX IF NOT EXISTS idx_organization_phones_org_id ON organization_phones(organization_id);
CREATE INDEX IF NOT EXISTS idx_organization_activities_org_id ON organization_activities(organization_id);
CREATE INDEX IF NOT EXISTS idx_organization_activities_activity_id ON organization_activities(activity_id);

-- Вставка тестовых данных для деятельностей (3 уровня вложенности)
INSERT INTO activities (name, parent_id, level) VALUES
-- Уровень 1
('Еда', NULL, 1),
('Автомобили', NULL, 1),
('IT услуги', NULL, 1),

-- Уровень 2 (подкатегории Еды)
('Мясная продукция', 1, 2),
('Молочная продукция', 1, 2),
('Хлебобулочные изделия', 1, 2),

-- Уровень 2 (подкатегории Автомобилей)
('Грузовые', 2, 2),
('Легковые', 2, 2),
('Запчасти', 2, 2),

-- Уровень 3 (подкатегории Запчастей)
('Аксессуары', 8, 3),
('Двигатели', 8, 3),
('Кузовные детали', 8, 3),

-- Уровень 2 (подкатегории IT услуг)
('Разработка ПО', 3, 2),
('Техническая поддержка', 3, 2),
('Облачные услуги', 3, 2),

-- Уровень 3 (подкатегории Разработки ПО)
('Веб-разработка', 13, 3),
('Мобильная разработка', 13, 3);

-- Вставка тестовых данных для зданий
INSERT INTO buildings (address, latitude, longitude) VALUES
('г. Москва, ул. Ленина 1, офис 3', 55.755826, 37.617300),
('г. Москва, ул. Тверская 25, офис 10', 55.760428, 37.606254),
('г. Москва, ул. Арбат 35, офис 5', 55.749592, 37.604826),
('г. Москва, пр. Мира 15, офис 20', 55.781773, 37.633324),
('г. Москва, ул. Новый Арбат 21, офис 8', 55.752023, 37.588272),
('г. Москва, ул. Блюхера 32/1', 55.788742, 37.590563);

-- Вставка тестовых данных для организаций
INSERT INTO organizations (name, building_id) VALUES
('ООО "Рога и Копыта"', 1),
('АО "Мясной двор"', 2),
('ИП "Молочные реки"', 3),
('ЗАО "АвтоГруз"', 4),
('ООО "Легковые авто"', 5),
('ИП "Запчасти оптом"', 6),
('ООО "IT Решения"', 1),
('АО "Техподдержка Плюс"', 2),
('ООО "Облачные технологии"', 3),
('ИП "ВебСтарт"', 4),
('ООО "Мобильные приложения"', 5),
('ООО "Хлебный дом"', 6);

-- Вставка тестовых данных для телефонов организаций
INSERT INTO organization_phones (organization_id, phone_number) VALUES
(1, '2-222-222'),
(1, '3-333-333'),
(1, '8-923-666-13-13'),
(2, '2-444-444'),
(2, '2-444-445'),
(3, '2-555-555'),
(4, '2-666-666'),
(5, '2-777-777'),
(6, '2-888-888'),
(7, '2-999-999'),
(8, '3-111-111'),
(9, '3-222-222'),
(10, '3-333-333'),
(11, '3-444-444'),
(12, '3-555-555');

-- Вставка тестовых данных для связи организаций и деятельностей
INSERT INTO organization_activities (organization_id, activity_id) VALUES
-- ООО "Рога и Копыта" - много видов деятельности
(1, 1), (1, 4), (1, 5),

-- АО "Мясной двор" - мясная продукция
(2, 4),

-- ИП "Молочные реки" - молочная продукция
(3, 5),

-- ЗАО "АвтоГруз" - автомобили, грузовые
(4, 2), (4, 7),

-- ООО "Легковые авто" - автомобили, легковые
(5, 2), (5, 8),

-- ИП "Запчасти оптом" - запчасти и аксессуары
(6, 8), (6, 9), (6, 10),

-- IT компании
(7, 3), (7, 13), (7, 16),
(8, 3), (8, 14),
(9, 3), (9, 15),
(10, 3), (10, 13), (10, 16),
(11, 3), (11, 13), (11, 17),

-- ООО "Хлебный дом" - хлебобулочные изделия
(12, 6);

-- Функция для получения всех дочерних деятельностей (рекурсивно)
CREATE OR REPLACE FUNCTION get_child_activities(parent_activity_id INTEGER)
RETURNS TABLE(activity_id INTEGER) AS $$
BEGIN
    RETURN QUERY 
    WITH RECURSIVE activity_tree AS (
        SELECT id, parent_id
        FROM activities 
        WHERE id = parent_activity_id OR (parent_activity_id IS NULL AND parent_id IS NULL)
        
        UNION ALL
        
        SELECT a.id, a.parent_id
        FROM activities a
        INNER JOIN activity_tree at ON a.parent_id = at.id
        WHERE a.level <= 3  -- Ограничение уровня вложенности
    )
    SELECT id FROM activity_tree;
END;
$$ LANGUAGE plpgsql;

-- Представление для удобного просмотра организаций с их данными
CREATE OR REPLACE VIEW organization_details AS
SELECT 
    o.id,
    o.name as organization_name,
    b.address,
    b.latitude,
    b.longitude,
    ARRAY_AGG(DISTINCT op.phone_number) as phone_numbers,
    ARRAY_AGG(DISTINCT a.name) as activity_names,
    COUNT(DISTINCT a.id) as activity_count
FROM organizations o
LEFT JOIN buildings b ON o.building_id = b.id
LEFT JOIN organization_phones op ON o.id = op.organization_id
LEFT JOIN organization_activities oa ON o.id = oa.organization_id
LEFT JOIN activities a ON oa.activity_id = a.id
GROUP BY o.id, o.name, b.address, b.latitude, b.longitude;