import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Sum

from apps.agencies.infrastructure.models import AgencyModel
from apps.listings.infrastructure.models import ListingModel
from apps.leads.infrastructure.models import LeadModel


@login_required
def mis_dashboard(request):
    agencies = AgencyModel.objects.filter(is_active=True).order_by("name")
    return render(request, "mis/dashboard.html", {"agencies": agencies})


@login_required
def agency_detail(request, agency_id):
    agency = get_object_or_404(AgencyModel, pk=agency_id)

    listings_qs = ListingModel.objects.filter(agency_id=agency_id)
    listings_by_status = dict(
        listings_qs.values_list("status").annotate(count=Count("id"))
    )
    total_views = listings_qs.aggregate(total=Sum("view_count"))["total"] or 0
    avg_price = listings_qs.aggregate(avg=Avg("price_chf"))["avg"] or 0

    leads_qs = LeadModel.objects.filter(agency_id=agency_id)
    lead_stats = leads_qs.values_list("status").annotate(count=Count("id"))

    context = {
        "agency": agency,
        "listings_by_status": listings_by_status,
        "total_listings": listings_qs.count(),
        "total_views": total_views,
        "avg_price": avg_price,
        "lead_stats": list(lead_stats),
        # Serialized to JSON so the template can emit valid JSON in data-props
        "price_calculator_props": json.dumps({
            "agencyId": str(agency.id),
            "canton": agency.canton,
            "avgPrice": float(avg_price),
        }),
    }
    return render(request, "mis/agency_detail.html", context)
