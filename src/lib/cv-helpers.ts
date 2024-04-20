import type { CollectionEntry } from "astro:content";

import dayjs from "./dayjs";

// based on private experience and to level out certain outliers
const SKILL_MODIFIERS = [
    { "Container": 1.9 },
    { "Cloud": 1.9 },
    { "Security": 2.2 },
    { "Automatisierung": 1.2 }
]

// aggregate tech skills into groups
const SKILL_GROUPS = [
    { label: "Frontend", skills: ["HTML/CSS", "JavaScript", "Angular"] },
    { label: "Backend", skills: ["Golang", "Node.JS", "Dotnet", "Python", "Django", "PHP"] },
    { label: "Cloud", skills: ["AWS", "Cloud-Migration", "Azure", "GCP"] },
    { label: "Container", skills: ["Docker", "Kubernetes", "Helm"] }
]

// define skill groups
const TECH_SKILLS = ["Frontend", "Backend", "Cloud", "Container", "Security", "Automatisierung"]
const METHOD_SKILLS = ["Agile", "SAFe", "Requirements Management", "Design Thinking", "Scrum", "Kanban", "Design Thinking"]

const getToolTip = (label: string) => {
    const idx = SKILL_GROUPS.findIndex(group => group.label === label);
    if (idx > -1) {
        return SKILL_GROUPS[idx].skills.join(", ");
    }
    return label;
}

const getMaxDays = (entries: CollectionEntry<"cv-entries">[]) => {
    const maxFromDate = entries.map(entry => entry.data.from).reduce((acc: Date, date: Date) => {
        return dayjs(date).isBefore(acc) ? date : acc;
    })
    return dayjs().diff(dayjs(maxFromDate), 'day');
}

const sortedTopN = (items: Record<string, number>, topN: number) => {
    return Object.entries(items)
        .sort((a, b) => b[1] - a[1])
        .slice(0, topN);
}

const getTopSkills = (entries: CollectionEntry<"cv-entries">[], topN = { tech: 5, method: 3 }) => {
    const maxDays = getMaxDays(entries);

    // get weighted skills from cv entries
    const weightedSkills = entries.reduce((acc: Record<string, number>, entry) => {
        // tracks if we already added a skill to avoid double counting
        const skillsAdded: string[] = []
        entry.data.skills.forEach((skill) => {
            const score = calculateSkillScore(entry, maxDays);
            // determine skill group if applicable
            const skillGroup = SKILL_GROUPS.find(group => group.skills.includes(skill))
            const targetKey = skillGroup?.label ?? skill;
            if (!acc[targetKey]) {
                acc[targetKey] = score;
            } else if (!skillsAdded.includes(skill)) { // prevents double counting of skills
                acc[targetKey] += score;
            }
            skillsAdded.push(...skillGroup?.skills ?? [skill]);
        });
        return acc;
    }, {});

    // apply modifiers
    SKILL_MODIFIERS.forEach((modifier) => {
        const skill = Object.keys(modifier)[0];
        const value = Object.values(modifier)[0];
        if (weightedSkills[skill]) {
            if (value < 0) {
                weightedSkills[skill] /= Math.abs(value)
            } else {
                weightedSkills[skill] *= value;
            }
        }
    });

    // split skills into group
    const groups: Record<string, Record<string, number>> = {
        "tech": Object.keys(weightedSkills).filter(skill => TECH_SKILLS.includes(skill)).map((key) => {
            return { [key]: weightedSkills[key] }
        }).reduce((acc, item) => {
            return { ...acc, ...item }
        }),
        "method": Object.keys(weightedSkills).filter(skill => METHOD_SKILLS.includes(skill)).map((key) => {
            return { [key]: weightedSkills[key] }
        }).reduce((acc, item) => {
            return { ...acc, ...item }
        })
    }

    // normalize scales
    Object.keys(groups).forEach((group) => {
        const maxScore = Math.max(...Object.values(groups[group])) * 1.1; // one never achieves perfection
        Object.keys(groups[group]).forEach((key) => {
            groups[group][key] = (groups[group][key] / maxScore) * 100;
        });
    })

    // return sorted top N skills
    return (
        {
            techSkills: sortedTopN(groups.tech, topN.tech),
            methodSkills: sortedTopN(groups.method, topN.method)
        }
    )
}

// calculate skill score based on its age
const calculateSkillScore = (entry: CollectionEntry<"cv-entries">, maxDays: number) => {
    const dayDiff = dayjs().diff(dayjs(entry.data.to ?? dayjs()), 'day');
    return 100 - Math.round((dayDiff / maxDays) * 100);
}

export {
    getTopSkills,
    getToolTip
}