import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Reporter, Issue, CriticalIssue, LowPriorityIssue

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTERS_FILE = os.path.join(BASE_DIR, "reporters.json")
ISSUES_FILE = os.path.join(BASE_DIR, "issues.json")


def load_json(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        return json.load(f)


def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


@csrf_exempt
def reporters(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            r = Reporter(
                id=data["id"],
                name=data["name"],
                email=data["email"],
                team=data["team"],
            )
            r.validate()
            all_reporters = load_json(REPORTERS_FILE)
            if any(x["id"] == r.id for x in all_reporters):
                return JsonResponse({"error": f"Reporter with id {r.id} already exists"}, status=400)
            all_reporters.append(r.to_dict())
            save_json(REPORTERS_FILE, all_reporters)
            return JsonResponse(r.to_dict(), status=201)
        except (KeyError, json.JSONDecodeError) as e:
            return JsonResponse({"error": f"Invalid request body: {e}"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == "GET":
        all_reporters = load_json(REPORTERS_FILE)
        reporter_id = request.GET.get("id")
        if reporter_id:
            try:
                rid = int(reporter_id)
            except ValueError:
                return JsonResponse({"error": "id must be an integer"}, status=400)
            for rep in all_reporters:
                if rep["id"] == rid:
                    return JsonResponse(rep, status=200)
            return JsonResponse({"error": "Reporter not found"}, status=404)
        return JsonResponse(all_reporters, safe=False, status=200)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def issues(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            priority = data.get("priority", "")
            if priority == "critical":
                issue = CriticalIssue(
                    id=data["id"],
                    title=data["title"],
                    description=data.get("description", ""),
                    status=data["status"],
                    priority=priority,
                    reporter_id=data["reporter_id"],
                )
            elif priority == "low":
                issue = LowPriorityIssue(
                    id=data["id"],
                    title=data["title"],
                    description=data.get("description", ""),
                    status=data["status"],
                    priority=priority,
                    reporter_id=data["reporter_id"],
                )
            else:
                issue = Issue(
                    id=data["id"],
                    title=data["title"],
                    description=data.get("description", ""),
                    status=data["status"],
                    priority=priority,
                    reporter_id=data["reporter_id"],
                )
            issue.validate()

            all_reporters = load_json(REPORTERS_FILE)
            if not any(r["id"] == issue.reporter_id for r in all_reporters):
                return JsonResponse({"error": f"Reporter with id {issue.reporter_id} not found"}, status=404)

            all_issues = load_json(ISSUES_FILE)
            if any(x["id"] == issue.id for x in all_issues):
                return JsonResponse({"error": f"Issue with id {issue.id} already exists"}, status=400)

            response_data = issue.to_dict()
            response_data["message"] = issue.describe()
            all_issues.append(issue.to_dict())
            save_json(ISSUES_FILE, all_issues)
            return JsonResponse(response_data, status=201)

        except (KeyError, json.JSONDecodeError) as e:
            return JsonResponse({"error": f"Invalid request body: {e}"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == "GET":
        all_issues = load_json(ISSUES_FILE)
        issue_id = request.GET.get("id")
        status_filter = request.GET.get("status")

        if issue_id:
            try:
                iid = int(issue_id)
            except ValueError:
                return JsonResponse({"error": "id must be an integer"}, status=400)
            for issue in all_issues:
                if issue["id"] == iid:
                    return JsonResponse(issue, status=200)
            return JsonResponse({"error": "Issue not found"}, status=404)

        if status_filter:
            filtered = [i for i in all_issues if i["status"] == status_filter]
            return JsonResponse(filtered, safe=False, status=200)

        return JsonResponse(all_issues, safe=False, status=200)

    return JsonResponse({"error": "Method not allowed"}, status=405)
