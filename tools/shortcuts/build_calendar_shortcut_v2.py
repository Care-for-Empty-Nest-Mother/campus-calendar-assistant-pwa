from pathlib import Path
import plistlib

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'calendar-sync-v2.1.xml'
SHORTCUT_NAME = 'calendar-sync-v2.1'

GET_CLIP = 'B2C3D4E0-1111-4A00-8B5A-0F8E2D3C4970'
TEXT = 'B2C3D4E1-2222-4B11-9C6B-10F9E3D4A081'
SPLIT_LINES = 'B2C3D4E2-3333-4C22-AD7C-21A0F4E5B192'
SPLIT_FIELDS = 'B2C3D4E3-4444-4D33-BE8D-32B1F5F6C2A3'
REPEAT_GROUP = 'B2C3D4E4-5555-4E44-CF9E-43C2F6A7D3B4'
REPEAT_START = 'B2C3D4E5-6666-4F55-DA0F-54D3A7B8E4C5'
REPEAT_END = 'B2C3D4E6-7777-4066-EB10-65E4B8C9F5D6'
VERB = 'B2C3D4E7-8888-4177-FC21-76F5C9DA06E7'
START = 'B2C3D4E8-9999-4288-0D32-87A6DAEB17F8'
END = 'B2C3D4E9-AAAA-4399-1E43-98B7EBFC2809'
TITLE = 'B2C3D4EA-BBBB-44AA-2F54-A9C8FC0D391A'
LOCATION = 'B2C3D4EB-CCCC-45BB-3065-BAD90D1E4A2B'
NOTES = 'B2C3D4EC-DDDD-46CC-4176-CBEA1E2F5B3C'
KIND = 'B2C3D4ED-EEEE-47DD-5287-DCFB2F306C4D'
CATEGORY = 'B2C3D4EE-FFFF-48EE-6398-ED0C30417D5E'
MARKER = 'B2C3D4EF-0000-49FF-74A9-FE1D41528E6F'
IF_CLEAR_GROUP = 'B2C3D4F0-1111-4A00-85BA-0F2E52639F70'
IF_CLEAR_START = 'B2C3D4F1-2222-4B11-96CB-103F6374A081'
IF_CLEAR_ELSE = 'B2C3D4F2-3333-4C22-A7DC-21407485B192'
CLEAR_START_DATE = 'B2C3D4F3-4444-4D33-B8ED-32518596C2A3'
CLEAR_END_DATE = 'B2C3D4F4-5555-4E44-C9FE-436296A7D3B4'
FILTER_CLEAR = 'B2C3D4F5-6666-4F55-DA0F-5473A7B8E4C5'
REMOVE_EVENTS = 'B2C3D4F6-7777-4066-EB10-6584B8C9F5D6'
IF_ALLDAY_GROUP = 'B2C3D4F7-8888-4177-FC21-7695C9DA06E7'
IF_ALLDAY_START = 'B2C3D4F8-9999-4288-0D32-87A6DAEB17F8'
EVENT_ALLDAY = 'B2C3D4F9-AAAA-4399-1E43-98B7EBFC2809'
IF_ALLDAY_ELSE = 'B2C3D4FA-BBBB-44AA-2F54-A9C8FC0D391A'
IF_ALLDAY_END = 'B2C3D502-3333-4C22-A7DC-21407485B192'
IF_DAY_GROUP = 'B2C3D4FB-CCCC-45BB-3065-BAD90D1E4A2B'
IF_DAY_START = 'B2C3D4FC-DDDD-46CC-4176-CBEA1E2F5B3C'
EVENT_DAY = 'B2C3D4FD-EEEE-47DD-5287-DCFB2F306C4D'
IF_DAY_ELSE = 'B2C3D4FE-FFFF-48EE-6398-ED0C30417D5E'
EVENT_SOON = 'B2C3D4FF-0000-49FF-74A9-FE1D41528E6F'
IF_DAY_END = 'B2C3D500-1111-4A00-85BA-0F2E52639F70'
IF_CLEAR_END = 'B2C3D501-2222-4B11-96CB-103F6374A081'
OBJECT_REPLACEMENT = '\ufffc'


def attachment(value):
    return {'Value': value, 'WFSerializationType': 'WFTextTokenAttachment'}


def token_string(attachment_value):
    return {
        'Value': {
            'attachmentsByRange': {'{0, 1}': attachment_value},
            'string': OBJECT_REPLACEMENT,
        },
        'WFSerializationType': 'WFTextTokenString',
    }


def output_attachment(name, uid):
    return attachment({
        'Aggrandizements': [],
        'OutputName': name,
        'OutputUUID': uid,
        'Type': 'ActionOutput',
    })


def output_text(name, uid):
    return token_string({
        'Aggrandizements': [],
        'OutputName': name,
        'OutputUUID': uid,
        'Type': 'ActionOutput',
    })


def repeat_item_text():
    return token_string({
        'Aggrandizements': [],
        'Type': 'Variable',
        'VariableName': 'Repeat Item',
    })


def condition_input(name, uid):
    return {
        'Type': 'Variable',
        'Variable': {
            'Value': {
                'Aggrandizements': [],
                'OutputName': name,
                'OutputUUID': uid,
                'Type': 'ActionOutput',
            },
            'WFSerializationType': 'WFTextTokenAttachment',
        },
    }


def get_item(uid, name, index):
    return {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.getitemfromlist',
        'WFWorkflowActionParameters': {
            'UUID': uid,
            'CustomOutputName': name,
            'WFInput': output_attachment('字段', SPLIT_FIELDS),
            'WFItemSpecifier': 'Item At Index',
            # 快捷指令界面中的列表索引从 1 开始。
            'WFItemIndex': index + 1,
        },
    }

def date_from_text(uid, text_output):
    return {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.date',
        'WFWorkflowActionParameters': {
            'UUID': uid,
            'WFDateActionMode': 'Specified Date',
            'WFDateActionDate': text_output,
        },
    }


def add_event(uid, alert=None, all_day=False):
    params = {
        'UUID': uid,
        'WFCalendarItemTitle': output_text('标题', TITLE),
        'WFCalendarItemLocation': output_text('地点', LOCATION),
        'WFCalendarItemNotes': output_text('备注', NOTES),
        'WFCalendarItemDates': True,
        'WFCalendarItemStartDate': output_text('开始', START),
        'WFCalendarItemAllDay': all_day,
        'WFCalendarItemShowComposer': False,
        'ShowComposeSheet': False,
        'WFShowWhenRun': False,
    }
    if not all_day:
        params['WFCalendarItemEndDate'] = output_text('结束', END)
    if alert:
        params['WFAlertTime'] = alert
    return {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.addnewevent',
        'WFWorkflowActionParameters': params,
    }


def clear_filter():
    return {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.filter.calendarevents',
        'WFWorkflowActionParameters': {
            'UUID': FILTER_CLEAR,
            'WFContentItemFilter': {
                'Value': {
                    'WFActionParameterFilterPrefix': 1,
                    'WFContentPredicateBoundedDate': False,
                    'WFActionParameterFilterTemplates': [
                        {
                            'Bounded': True,
                            'Operator': 1003,
                            'Property': 'Start Date',
                            'Removable': False,
                            'Values': {
                                'AnotherDate': output_attachment('Date', CLEAR_END_DATE),
                                'Date': output_attachment('Date', CLEAR_START_DATE),
                                'Number': 7,
                                'Unit': 16,
                            },
                        },
                        {
                            'Operator': 99,
                            'Property': 'Notes',
                            'Removable': True,
                            'Values': {
                                'String': output_text('标记', MARKER),
                            },
                        },
                    ],
                },
                'WFSerializationType': 'WFContentPredicateTableTemplate',
            },
        },
    }


def remove_events():
    return {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.removeevents',
        'WFWorkflowActionParameters': {
            'WFInputEvents': output_attachment('Calendar Events', FILTER_CLEAR),
            'WFCalendarIncludeFutureEvents': False,
        },
    }


actions = [
    {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.comment',
        'WFWorkflowActionParameters': {
            'WFCommentActionText': '校历小助手：先清除所选类别与日期范围的本助手日程，再批量写入新的日程。'
        },
    },
    {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.getclipboard',
        'WFWorkflowActionParameters': {'UUID': GET_CLIP},
    },
    {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.gettext',
        'WFWorkflowActionParameters': {
            'UUID': TEXT,
            'CustomOutputName': '日历指令',
            'WFTextActionText': output_text('Clipboard', GET_CLIP),
        },
    },
    {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.text.split',
        'WFWorkflowActionParameters': {
            'UUID': SPLIT_LINES,
            'CustomOutputName': '行',
            'text': output_text('日历指令', TEXT),
            'WFTextSeparator': 'New Lines',
        },
    },
    {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.repeat.each',
        'WFWorkflowActionParameters': {
            'UUID': REPEAT_START,
            'GroupingIdentifier': REPEAT_GROUP,
            'WFControlFlowMode': 0,
            'WFInput': output_attachment('行', SPLIT_LINES),
        },
    },
    {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.text.split',
        'WFWorkflowActionParameters': {
            'UUID': SPLIT_FIELDS,
            'CustomOutputName': '字段',
            'text': repeat_item_text(),
            'WFTextSeparator': 'Custom',
            'WFTextCustomSeparator': '|',
        },
    },
    get_item(VERB, '操作', 0),
    get_item(START, '开始', 1),
    get_item(END, '结束', 2),
    get_item(TITLE, '标题', 3),
    get_item(LOCATION, '地点', 4),
    get_item(NOTES, '备注', 5),
    get_item(KIND, '类型', 6),
    get_item(CATEGORY, '类别', 7),
    get_item(MARKER, '标记', 8),
    {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.conditional',
        'WFWorkflowActionParameters': {
            'UUID': IF_CLEAR_START,
            'GroupingIdentifier': IF_CLEAR_GROUP,
            'WFControlFlowMode': 0,
            'WFCondition': 4,
            'WFConditionalActionString': 'CLEAR',
            'WFInput': condition_input('操作', VERB),
        },
    },
    date_from_text(CLEAR_START_DATE, output_text('开始', START)),
    date_from_text(CLEAR_END_DATE, output_text('结束', END)),
    clear_filter(),
    remove_events(),
    {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.conditional',
        'WFWorkflowActionParameters': {
            'UUID': IF_CLEAR_ELSE,
            'GroupingIdentifier': IF_CLEAR_GROUP,
            'WFControlFlowMode': 1,
        },
    },
    {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.conditional',
        'WFWorkflowActionParameters': {
            'UUID': IF_ALLDAY_START,
            'GroupingIdentifier': IF_ALLDAY_GROUP,
            'WFControlFlowMode': 0,
            'WFCondition': 4,
            'WFConditionalActionString': 'allday',
            'WFInput': condition_input('类型', KIND),
        },
    },
    add_event(EVENT_ALLDAY, all_day=True),
    {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.conditional',
        'WFWorkflowActionParameters': {
            'UUID': IF_ALLDAY_ELSE,
            'GroupingIdentifier': IF_ALLDAY_GROUP,
            'WFControlFlowMode': 1,
        },
    },
    {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.conditional',
        'WFWorkflowActionParameters': {
            'UUID': IF_DAY_START,
            'GroupingIdentifier': IF_DAY_GROUP,
            'WFControlFlowMode': 0,
            'WFCondition': 4,
            'WFConditionalActionString': 'day',
            'WFInput': condition_input('类型', KIND),
        },
    },
    add_event(EVENT_DAY, alert='1 day before'),
    {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.conditional',
        'WFWorkflowActionParameters': {
            'UUID': IF_DAY_ELSE,
            'GroupingIdentifier': IF_DAY_GROUP,
            'WFControlFlowMode': 1,
        },
    },
    add_event(EVENT_SOON, alert='15 minutes before'),
    {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.conditional',
        'WFWorkflowActionParameters': {
            'UUID': IF_DAY_END,
            'GroupingIdentifier': IF_DAY_GROUP,
            'WFControlFlowMode': 2,
        },
    },
    {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.conditional',
        'WFWorkflowActionParameters': {
            'UUID': IF_ALLDAY_END,
            'GroupingIdentifier': IF_ALLDAY_GROUP,
            'WFControlFlowMode': 2,
        },
    },
    {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.conditional',
        'WFWorkflowActionParameters': {
            'UUID': IF_CLEAR_END,
            'GroupingIdentifier': IF_CLEAR_GROUP,
            'WFControlFlowMode': 2,
        },
    },
    {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.repeat.each',
        'WFWorkflowActionParameters': {
            'UUID': REPEAT_END,
            'GroupingIdentifier': REPEAT_GROUP,
            'WFControlFlowMode': 2,
        },
    },
]

workflow = {
    'WFWorkflowActions': actions,
    'WFWorkflowClientRelease': '26A0000a',
    'WFWorkflowClientVersion': '2700.0.4',
    'WFWorkflowIcon': {
        'WFWorkflowIconGlyphNumber': 59675,
        'WFWorkflowIconStartColor': 4282601983,
    },
    'WFWorkflowImportQuestions': [],
    'WFWorkflowInputContentItemClasses': [],
    'WFWorkflowMinimumClientVersion': 900,
    'WFWorkflowMinimumClientVersionString': '900',
    'WFWorkflowName': SHORTCUT_NAME,
    'WFWorkflowOutputContentItemClasses': [],
    'WFWorkflowTypes': [],
}

with OUT.open('wb') as f:
    plistlib.dump(workflow, f, fmt=plistlib.FMT_XML, sort_keys=False)
print(OUT)
