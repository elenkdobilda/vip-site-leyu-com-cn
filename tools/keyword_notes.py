from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

sample_url = "https://vip-site-leyu.com.cn"
sample_keyword = "乐鱼体育"


@dataclass
class KeywordNote:
    keyword: str
    url: str
    description: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def update_description(self, new_description: str) -> None:
        self.description = new_description
        self.updated_at = datetime.now()

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "url": self.url,
            "description": self.description,
            "tags": self.tags.copy(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


@dataclass
class KeywordGroup:
    name: str
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def remove_note(self, keyword: str) -> bool:
        for idx, note in enumerate(self.notes):
            if note.keyword == keyword:
                del self.notes[idx]
                return True
        return False

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [note for note in self.notes if tag in note.tags]


def format_notes_table(notes: List[KeywordNote]) -> str:
    if not notes:
        return "（无笔记）"

    lines = ["+----------------------+------------------------------------------+", 
             "| Keyword              | URL                                      |",
             "+----------------------+------------------------------------------+"]
    for note in notes:
        kw = note.keyword[:22].ljust(22)
        url = note.url[:40].ljust(40)
        lines.append(f"| {kw} | {url} |")
        if note.description:
            desc = note.description[:60].ljust(60)
            lines.append(f"| Description: {desc} |")
        if note.tags:
            tags_str = ", ".join(note.tags)[:56].ljust(56)
            lines.append(f"| Tags: {tags_str} |")
        lines.append("+----------------------+------------------------------------------+")
    return "\n".join(lines)


def format_notes_json(notes: List[KeywordNote]) -> str:
    import json
    data = [note.to_dict() for note in notes]
    return json.dumps(data, ensure_ascii=False, indent=2)


def generate_summary(group: KeywordGroup) -> str:
    total = len(group.notes)
    all_tags = set()
    for note in group.notes:
        all_tags.update(note.tags)
    return f"组 '{group.name}': {total} 条笔记, {len(all_tags)} 个不同标签"


# 示例数据
if __name__ == "__main__":
    note1 = KeywordNote(
        keyword=sample_keyword,
        url=sample_url,
        description="体育资讯与赛事平台",
        tags=["体育", "娱乐"]
    )
    note2 = KeywordNote(
        keyword="足球直播",
        url=sample_url + "/live",
        description="实时足球比赛直播",
        tags=["足球", "直播", "体育"]
    )
    note3 = KeywordNote(
        keyword="篮球比分",
        url=sample_url + "/basketball",
        description="NBA/CBA比分更新",
        tags=["篮球", "比分"]
    )

    group = KeywordGroup(name="体育关键词")
    group.add_note(note1)
    group.add_note(note2)
    group.add_note(note3)

    print("=== 表格输出 ===")
    print(format_notes_table(group.notes))

    print("\n=== JSON输出 ===")
    print(format_notes_json(group.notes))

    print(f"\n=== 摘要 ===")
    print(generate_summary(group))

    print(f"\n=== 按标签查询 '体育' ===")
    for n in group.find_by_tag("体育"):
        print(f"  - {n.keyword}: {n.url}")