# Generated by Django 4.2.1 on 2024-05-14 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_demographics_current_phase_preop_phase2_phase1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='preop',
            old_name='hop_trial_1',
            new_name='hop_trial_1_affected',
        ),
        migrations.RenameField(
            model_name='preop',
            old_name='hop_trial_2',
            new_name='hop_trial_1_non_affected',
        ),
        migrations.AddField(
            model_name='preop',
            name='hop_trial_2_affected',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='preop',
            name='hop_trial_2_non_affected',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='dob',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='preop',
            name='percentage',
            field=models.IntegerField(null=True),
        ),
        migrations.CreateModel(
            name='Phase4',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.IntegerField(null=True)),
                ('draft', models.BooleanField(default=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('dominant_leg', models.CharField(blank=True, max_length=50, null=True)),
                ('swelling', models.CharField(blank=True, max_length=50, null=True)),
                ('stability', models.CharField(blank=True, max_length=50, null=True)),
                ('flexion', models.CharField(blank=True, max_length=50, null=True)),
                ('extension', models.CharField(blank=True, max_length=50, null=True)),
                ('aclrsi_q1', models.IntegerField(null=True)),
                ('aclrsi_q2', models.IntegerField(null=True)),
                ('aclrsi_q3', models.IntegerField(null=True)),
                ('ikdc_q1', models.IntegerField(null=True)),
                ('ikdc_q2', models.IntegerField(null=True)),
                ('ikdc_q3', models.CharField(null=True)),
                ('tsk_q1', models.IntegerField(null=True)),
                ('tsk_q2', models.IntegerField(null=True)),
                ('tsk_q3', models.IntegerField(null=True)),
                ('result', models.CharField(blank=True, max_length=50, null=True)),
                ('forward_affected', models.FloatField(null=True)),
                ('forward_non_affected', models.FloatField(null=True)),
                ('forward_symmetry', models.FloatField(null=True)),
                ('postereomedical_affected', models.FloatField(null=True)),
                ('postereomedical_non_affected', models.FloatField(null=True)),
                ('postereolateral_affected', models.FloatField(null=True)),
                ('postereolateral_non_affected', models.FloatField(null=True)),
                ('postereo_symmetry', models.FloatField(null=True)),
                ('cooper_side_affected', models.CharField(blank=True, max_length=50, null=True)),
                ('cooper_side_non_affected', models.CharField(blank=True, max_length=50, null=True)),
                ('cooper_up_affected', models.CharField(blank=True, max_length=50, null=True)),
                ('cooper_up_non_affected', models.CharField(blank=True, max_length=50, null=True)),
                ('hop_trial_1_affected', models.FloatField(null=True)),
                ('hop_trial_1_non_affected', models.FloatField(null=True)),
                ('hop_trial_2_affected', models.FloatField(null=True)),
                ('hop_trial_2_non_affected', models.FloatField(null=True)),
                ('hop_symmetry', models.FloatField(null=True)),
                ('triple_trial_1_affected', models.FloatField(null=True)),
                ('triple_trial_1_non_affected', models.FloatField(null=True)),
                ('triple_trial_2_affected', models.FloatField(null=True)),
                ('triple_trial_2_non_affected', models.FloatField(null=True)),
                ('triple_symmetry', models.FloatField(null=True)),
                ('crossover_trial_1_affected', models.FloatField(null=True)),
                ('crossover_trial_1_non_affected', models.FloatField(null=True)),
                ('crossover_trial_2_affected', models.FloatField(null=True)),
                ('crossover_trial_2_non_affected', models.FloatField(null=True)),
                ('crossover_symmetry', models.FloatField(null=True)),
                ('side_trial_1_affected', models.FloatField(null=True)),
                ('side_trial_1_non_affected', models.FloatField(null=True)),
                ('side_symmetry', models.FloatField(null=True)),
                ('repetitions_affected', models.FloatField(null=True)),
                ('repetitions_non_affected', models.FloatField(null=True)),
                ('repetition_symmetry', models.FloatField(null=True)),
                ('test_1_name', models.CharField(blank=True, max_length=50, null=True)),
                ('test_1_result', models.CharField(blank=True, max_length=50, null=True)),
                ('test_1_baseline', models.CharField(blank=True, max_length=50, null=True)),
                ('test_1_pass', models.CharField(blank=True, max_length=50, null=True)),
                ('test_2_name', models.CharField(blank=True, max_length=50, null=True)),
                ('test_2_result', models.CharField(blank=True, max_length=50, null=True)),
                ('test_2_baseline', models.CharField(blank=True, max_length=50, null=True)),
                ('test_2_pass', models.CharField(blank=True, max_length=50, null=True)),
                ('fatigued_hop_trial_1_affected', models.FloatField(null=True)),
                ('fatigued_hop_trial_1_non_affected', models.FloatField(null=True)),
                ('fatigued_hop_trial_2_affected', models.FloatField(null=True)),
                ('fatigued_hop_trial_2_non_affected', models.FloatField(null=True)),
                ('fatigued_hop_symmetry', models.FloatField(null=True)),
                ('fatigued_triple_trial_1_affected', models.FloatField(null=True)),
                ('fatigued_triple_trial_1_non_affected', models.FloatField(null=True)),
                ('fatigued_triple_trial_2_affected', models.FloatField(null=True)),
                ('fatigued_triple_trial_2_non_affected', models.FloatField(null=True)),
                ('fatigued_triple_symmetry', models.FloatField(null=True)),
                ('fatigued_side_trial_1_affected', models.FloatField(null=True)),
                ('fatigued_side_trial_1_non_affected', models.FloatField(null=True)),
                ('fatigued_side_symmetry', models.FloatField(null=True)),
                ('sport_score', models.FloatField(null=True)),
                ('sport_hurdle', models.FloatField(null=True)),
                ('Demographics', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.demographics')),
            ],
        ),
        migrations.CreateModel(
            name='Phase3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.IntegerField(null=True)),
                ('draft', models.BooleanField(default=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('hop_trial_1_affected', models.FloatField(null=True)),
                ('hop_trial_1_non_affected', models.FloatField(null=True)),
                ('hop_trial_2_affected', models.FloatField(null=True)),
                ('hop_trial_2_non_affected', models.FloatField(null=True)),
                ('hop_symmetry', models.FloatField(null=True)),
                ('baseline_result', models.FloatField(null=True)),
                ('affected_limb', models.FloatField(null=True)),
                ('baseline_eq', models.CharField(blank=True, max_length=50, null=True)),
                ('triple_trial_1_affected', models.FloatField(null=True)),
                ('triple_trial_1_non_affected', models.FloatField(null=True)),
                ('triple_trial_2_affected', models.FloatField(null=True)),
                ('triple_trial_2_non_affected', models.FloatField(null=True)),
                ('crossover_trial_1_affected', models.FloatField(null=True)),
                ('crossover_trial_1_non_affected', models.FloatField(null=True)),
                ('crossover_trial_2_affected', models.FloatField(null=True)),
                ('crossover_trial_2_non_affected', models.FloatField(null=True)),
                ('crossover_symmetry', models.FloatField(null=True)),
                ('side_trial_1_affected', models.FloatField(null=True)),
                ('side_trial_1_non_affected', models.FloatField(null=True)),
                ('side_symmetry', models.FloatField(null=True)),
                ('triple_symmetry', models.FloatField(null=True)),
                ('repetitions_affected', models.FloatField(null=True)),
                ('repetitions_non_affected', models.FloatField(null=True)),
                ('repetition_symmetry', models.FloatField(null=True)),
                ('repetition_hurdle', models.CharField(blank=True, max_length=50, null=True)),
                ('star_forward_affected', models.FloatField(null=True)),
                ('star_forward_non_affected', models.FloatField(null=True)),
                ('star_forward_symmetry', models.FloatField(null=True)),
                ('postereomedical_affected', models.FloatField(null=True)),
                ('postereomedical_non_affected', models.FloatField(null=True)),
                ('postereolateral_affected', models.FloatField(null=True)),
                ('postereolateral_non_affected', models.FloatField(null=True)),
                ('postereo_symmetry', models.FloatField(null=True)),
                ('cooper_side_affected', models.CharField(blank=True, max_length=50, null=True)),
                ('cooper_side_non_affected', models.CharField(blank=True, max_length=50, null=True)),
                ('cooper_up_affected', models.CharField(blank=True, max_length=50, null=True)),
                ('cooper_up_non_affected', models.CharField(blank=True, max_length=50, null=True)),
                ('weight', models.FloatField(null=True)),
                ('leg_rm_affected', models.FloatField(null=True)),
                ('leg_rm_non_affected', models.FloatField(null=True)),
                ('leg_weight_affected', models.FloatField(null=True)),
                ('leg_weight_non_affected', models.FloatField(null=True)),
                ('squat_rm', models.FloatField(null=True)),
                ('squat_weight', models.FloatField(null=True)),
                ('Demographics', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.demographics')),
            ],
        ),
    ]
