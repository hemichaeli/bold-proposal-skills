# Stage 4c — Operations & Logistics Reference

## Purpose

A brilliant concept with broken logistics dies in execution. Stage 4c is where the event becomes a physical, buildable thing. The operations document is the production team's bible. It must be specific enough that a stranger could walk in and execute.

Output: `04-specialists/operations/logistics.md`

---

## The seven operational pillars

Every event proposal covers these seven areas. Some are brief, some are heavy, but none is absent.

### 1. Guest flow (זרימת קהל)

How guests move through the event, from the moment they leave their car to the moment they leave the venue. Map the journey as a sequence of zones. For each zone:
- What is it called (internally and externally)?
- What happens there?
- How many people can it hold?
- What is the dwell time?
- What is the transition out of it (signal, usher, doors open)?

### 2. Build and site plan (בינוי וצורת שטח)

The physical structures and dressings being built on site. Stage, bar, signage, installations, furniture, floor plan. Dimensions. What is rented, what is built custom, what is already there. Load-in and load-out times.

### 3. Technical infrastructure (תשתיות טכניות)

Sound, light, video, power. What is the system, who is the supplier (role, not name yet — actual vendors get priced in stage 5), what is the redundancy plan.

### 4. Safety, security, accessibility (בטיחות, אבטחה, נגישות)

Permits. Emergency exits. Security personnel. Medical coverage for events above a threshold (usually 300+ guests or events serving alcohol heavily). Wheelchair access, ramps, accessible restrooms. Weather contingency for outdoor.

### 5. Parking and transportation (חניה ותחבורה)

Capacity. Valet vs. self. Shuttle if remote. Drop-off zone. Accessibility for mobility-limited guests.

### 6. Staffing (צוות)

Roles (not names yet): event manager, stage manager, technical lead, runner coordinator, waitstaff supervisor, host/hostess team, security lead, first aid. Headcount per role. Call times.

### 7. Risk register (ניהול סיכונים)

What can go wrong. What is the mitigation. Top risks only (5 to 8). Not a full FMEA — this is a proposal, not a contract.

---

## Output template

```markdown
# Operations & Logistics — [שם אירוע]

## 1. זרימת הקהל

### מפת מסע
1. **הגעה לחניה** → 2. **עמדת כניסה** → 3. **אזור משקה פתיחה** → 4. **האולם הראשי** → 5. **מעבר/הפסקה** → 6. **השיא** → 7. **סיום / יציאה מבוקרת**

### פירוט לכל אזור

#### אזור 1: כניסה (arrival)
- **מיקום:** [...]
- **קיבולת מקבילית:** X אנשים
- **שהות ממוצעת:** X דק'
- **פעילות:** קבלת שמות, סימון רשימה, איסוף תג/מתנה
- **צוות:** 3 אושרים + 2 מאבטחים
- **עיצוב/מוטיב:** [איך המוטיב של brand-system מתבטא כאן]
- **מעבר החוצה:** איתות קולי + פתיחת דלתות לאולם

#### אזור 2: ...
(לכל אזור)

### צוואר בקבוק צפוי
[הזמן/המקום הצפוי להיות עמוס - כניסה ב-19:30? יציאה מהשיא? - ומה המענה]

## 2. בינוי ותכנון שטח

### תוכנית השטח (Floor plan)
[תיאור מילולי של החלוקה. אם יש מקום, ASCII diagram או קישור ל-Figma/sketch]

### רשימת בינוי
| פריט | מידות | בנוי/שכור | ספק (תפקיד) | הערות |
|---|---|---|---|---|
| במה ראשית | 6x4 מ' | שכור | חברת במות | גובה 60 ס"מ |
| קיר Reveal | 4x3 מ' | בנוי מותאם | נגר+מעצב | כולל מנגנון הסרה |
| בר ראשי | 5 מ' ארוך | שכור | ציוד אירוח | כולל קירור |
| שילוט ראשי | 2x1 מ' | מודפס | דפוס | ויניל על PVC |

### לוחות זמנים של הבינוי
- **Load-in:** [שעה, תאריך]
- **מוכן לבדיקה:** [שעה]
- **רהרסל ראשון:** [שעה]
- **פתיחת שערים:** [שעה]
- **Load-out:** [שעה, תאריך]

## 3. תשתיות טכניות

### סאונד
- **מערכת:** [תיאור: PA ראשי, מוניטורים, מיקרופונים]
- **ספק (תפקיד):** חברת הגברה
- **בקרה:** עמדת FOH עם סאונדמן חי
- **גיבוי:** מיקרופון נוסף, רמקול ניידים

### אור
- **תכנון תאורה:** [תיאור - דרמטי / רך / צבעוני / שלבים]
- **ציוד:** [ביס, spots, ambient, moving heads, haze]
- **ספק (תפקיד):** מעצב תאורה + חברת תאורה
- **בקרה:** מפעיל אור חי
- **גיבוי חירום:** תאורת חירום חוקית

### וידאו ופרויקטור
- **מסכים:** [LED wall 4x3? מסכי פלזמה? מקרן?]
- **ספק (תפקיד):** חברת וידאו
- **תוכן:** פרזנטציה, לוגואים, הקרנות, תמונות חיות
- **בקרה:** video switcher

### חשמל
- **עומס מחושב:** [X קילוואט]
- **מקור:** חיבור קבוע בחצר + גנרטור גיבוי עבור X ק"ו
- **ספק (תפקיד):** חברת חשמל אירועים / חשמלאי אחראי

### קישוריות
- **Wi-Fi:** [לצוות / לקהל? רוחב פס?]
- **חיבור לרשת/סטרימינג:** [אם רלוונטי]

## 4. בטיחות, אבטחה, נגישות

### היתרים נדרשים
- [רישיון עסק, היתר התקהלות, היתר כיבוי אש, אישור מהנדס בטיחות, היתר משטרה אם נדרש]

### אבטחה
- **מספר מאבטחים:** [בהתאם לרגולציה ולמספר האורחים]
- **חברת אבטחה (תפקיד):** [...]
- **תפקידים:** כניסה, פטרול פנים, חצר/חניה

### שירותי רפואה
- **חובה:** [כן/לא, לפי רגולציה]
- **נוכחות:** [חובש/פרמדיק/אמבולנס]
- **ספק (תפקיד):** [...]

### נגישות
- **מעלית/רמפה לכיסאות גלגלים:** [מצב]
- **שירותי נכים:** [מצב]
- **ליווי סומים/כבדי שמיעה:** [אם רלוונטי]

## 5. חניה ותחבורה

- **קיבולת חניה:** [X מקומות]
- **סוג:** עצמי / valet / שירותי / שילוב
- **drop-off:** [מיקום + תיאום שוטר/מאבטח]
- **שאטלים:** [אם רלוונטי, מאיפה לאן]
- **תחבורה ציבורית בקרבת מקום:** [לציון אם רלוונטי]

## 6. צוות

| תפקיד | מספר | זמן קריאה | אחריות |
|---|---|---|---|
| מנהל אירוע (Event Manager) | 1 | Load-in | בעלות כוללת |
| מנהל במה (Stage Manager) | 1 | 3 שעות לפני אורחים | Cue, תזמון, MC |
| טכנאי סאונד | 1 | Load-in | מערכת + סאונד חי |
| טכנאי תאורה | 1 | Load-in | בקרת אור חיה |
| טכנאי וידאו | 1 | Load-in | בקרת מסכים + הקרנות |
| Runner | 2 | שעה לפני | שליחויות, גיבוי |
| מלצרים/ברמנים | [לפי מוזמנים: 1:20] | 90 דק' לפני | הגשה |
| אושרים (hosts) | 4 | 45 דק' לפני | קבלה, הכוונה |
| מאבטחים | [לפי רגולציה] | 45 דק' לפני | אבטחה |
| חובש | 1 | שעה לפני | רפואה |

## 7. ניהול סיכונים

| סיכון | סבירות | חומרה | מענה |
|---|---|---|---|
| גשם (אם חיצוני) | בינונית | גבוהה | אוהל/טנט, plan B פנימי |
| איחור אורחים מרכזיים | גבוהה | בינונית | חלון גמישות של 15 דק' בפתיחה |
| תקלת הגברה | נמוכה | גבוהה | מערכת גיבוי, מיקרופון חלופי |
| עומס יתר בכניסה | בינונית | בינונית | 2 עמדות כניסה במקביל |
| ביטול דובר ברגע אחרון | נמוכה | גבוהה | דובר גיבוי מוכן (או סרטון הוקלט מראש) |

## 8. הערות לתקציב (transitions to stage 5)

בכל פעם שרשימת ציוד או תפקיד מופיעה מעלה, היא צריכה להפוך לשורת תקציב בשלב 5. הערות לא-טריוויאליות:
- [אם יש ציוד יוצא דופן או תפקיד שדורש חישוב מיוחד]
```

---

## Site-specific adjustments

### Outdoor events
- Weather plan is mandatory, not optional.
- Sound permits and curfew (usually 22:00 or 23:00 in Israel) shape the agenda.
- Mosquito/insect mitigation in summer.
- Wind plan for any tall structures.

### Indoor events with catering kitchen
- Kitchen access times coordinate with catering load-in, not with general load-in.
- Smoke detector deactivation (if sparklers or dramatic smoke) requires venue approval.

### Events with VIPs
- Dedicated green room.
- Separate arrival route if possible.
- Private security coordination.

### Hybrid or streamed events
- Stream infrastructure becomes a whole additional pillar. Cameras, switcher, streaming platform, connectivity redundancy.

---

## What "done" looks like

A production manager reading this file should know:
- Where every person is at every moment.
- What equipment is on site, from whom, when.
- What happens if it rains / the speaker is late / the power drops.

If any of those are ambiguous, the document is not yet done.
